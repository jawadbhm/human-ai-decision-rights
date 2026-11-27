"""Offline decision-rights prototype. Standard library only; no live systems or LLM calls."""
from dataclasses import dataclass, replace
import csv, json
from pathlib import Path

@dataclass(frozen=True)
class Request:
    tier:int
    action:str='execute' # draft, decide, execute
    actor:str='agent'
    owner:str='Function owner'
    within_scope:bool=True
    anomaly:bool=False
    review:bool=False
    authorized:bool=False
    risk_approved:bool=False
    eval_pass:bool=True
    audit_available:bool=True
    kill_switch:bool=False
    rollback_ready:bool=True
    protected:bool=False
    fail_after_write:bool=False

def gate(r):
    if r.kill_switch: return 'BLOCK', 'kill switch active'
    if not r.audit_available: return 'BLOCK', 'audit unavailable'
    if not r.owner: return 'ESCALATE', 'accountable owner missing'
    if r.tier not in (1,2,3,4): return 'BLOCK','unknown tier'
    if r.action not in ('draft','decide','execute') or r.actor not in ('agent','human'): return 'BLOCK','invalid action or actor'
    if not r.within_scope or r.anomaly: return 'ESCALATE','scope exception or anomaly'
    if r.action=='draft': return 'ALLOW','non-executing assistance'
    if r.protected or r.tier==4:
        return ('ALLOW','authorized human approval') if r.actor=='human' and r.authorized and r.review else ('BLOCK','human-only decision or execution')
    if r.tier==1:
        return ('ALLOW','human-reviewed execution') if r.actor=='human' and r.review and r.authorized else ('BLOCK','assisted tier requires authorized human review and execution')
    if r.actor=='human':
        return ('ALLOW','authorized human') if r.authorized and r.review else ('BLOCK','human authorization and review missing')
    if r.tier==2:
        return ('ALLOW','bounded execution') if r.action=='execute' else ('ESCALATE','decision outside bounded remit')
    if r.action!='execute': return 'ESCALATE','decision outside delegated remit'
    if not (r.risk_approved and r.eval_pass and r.rollback_ready): return 'ESCALATE','risk approval, eval, or rollback gate missing'
    return 'ALLOW','delegated execution approved'

def run(r, case):
    decision, reason=gate(r)
    state={'record':'original'}
    before=state.copy()
    if decision=='ALLOW' and r.action=='execute':
        state['record']='updated'
        if r.fail_after_write:
            # The mock transactional executor restores its initial state.
            state=before.copy()
            decision,reason='ROLLBACK','injected downstream failure; prior state restored'
    return {'case':case,'tier':r.tier,'actor':r.actor,'action':r.action,'decision':decision,'reason':reason,'owner':r.owner,'state_changed':state!=before,'audit_available':r.audit_available}

T1=Request(1); T2=Request(2); T3=Request(3,risk_approved=True); T4=Request(4)
H=dict(actor='human',review=True,authorized=True)
# Hand-authored test oracles; deliberately exercise each tier and cross-tier controls.
cases=[
('T1 draft summary',replace(T1,action='draft'),'ALLOW',False),
('T1 agent sends email',T1,'BLOCK',False),
('T1 human reviewed send',replace(T1,**H),'ALLOW',True),
('T1 human skips review',replace(T1,actor='human',authorized=True),'BLOCK',False),
('T1 missing owner',replace(T1,owner=''),'ESCALATE',False),
('T1 agent decides',replace(T1,action='decide'),'BLOCK',False),
('T1 scope exception',replace(T1,action='draft',within_scope=False),'ESCALATE',False),
('T1 kill switch',replace(T1,action='draft',kill_switch=True),'BLOCK',False),
('T2 routine ticket update',T2,'ALLOW',True),
('T2 out of scope',replace(T2,within_scope=False),'ESCALATE',False),
('T2 anomaly alert',replace(T2,anomaly=True),'ESCALATE',False),
('T2 missing owner',replace(T2,owner=''),'ESCALATE',False),
('T2 unbounded decision',replace(T2,action='decide'),'ESCALATE',False),
('T2 protected pay update',replace(T2,protected=True),'BLOCK',False),
('T2 audit outage',replace(T2,audit_available=False),'BLOCK',False),
('T2 authorized human exception resolution',replace(T2,**H),'ALLOW',True),
('T3 approved cross-system update',T3,'ALLOW',True),
('T3 missing risk approval',replace(T3,risk_approved=False),'ESCALATE',False),
('T3 failed eval',replace(T3,eval_pass=False),'ESCALATE',False),
('T3 missing rollback plan',replace(T3,rollback_ready=False),'ESCALATE',False),
('T3 kill switch',replace(T3,kill_switch=True),'BLOCK',False),
('T3 missing audit',replace(T3,audit_available=False),'BLOCK',False),
('T3 protected reorganization',replace(T3,protected=True),'BLOCK',False),
('T3 injected execution failure',replace(T3,fail_after_write=True),'ROLLBACK',False),
('T4 compensation scenario draft',replace(T4,action='draft'),'ALLOW',False),
('T4 agent approves compensation',replace(T4,action='decide'),'BLOCK',False),
('T4 agent changes compensation',T4,'BLOCK',False),
('T4 authorized human decision',replace(T4,action='decide',**H),'ALLOW',False),
('T4 authorized human execution',replace(T4,**H),'ALLOW',True),
('T4 unauthorized human',replace(T4,actor='human',review=True),'BLOCK',False),
('T4 human missing approval',replace(T4,actor='human',authorized=True),'BLOCK',False),
('T4 missing owner',replace(T4,action='draft',owner=''),'ESCALATE',False),
]
if __name__=='__main__':
    results=[]
    for name,r,expected,changed in cases:
        result=run(r,name)
        result.update(expected_decision=expected,expected_state_changed=changed,passed=(result['decision']==expected and result['state_changed']==changed))
        results.append(result)
    p=Path(__file__).resolve().parent
    with (p/'results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(results[0])); w.writeheader(); w.writerows(results)
    counts={x:sum(r['decision']==x for r in results) for x in ('ALLOW','BLOCK','ESCALATE','ROLLBACK')}
    report={'cases':len(results),'passed':sum(r['passed'] for r in results),'decisions':counts,'unexpected_state_changes':sum(r['state_changed'] and not r['expected_state_changed'] for r in results),'allowed_executions':sum(r['state_changed'] for r in results),'per_tier':{str(t):{'cases':sum(r['tier']==t for r in results),'passed':sum(r['tier']==t and r['passed'] for r in results)} for t in range(1,5)}}
    (p/'summary.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
    assert report['passed']==report['cases']

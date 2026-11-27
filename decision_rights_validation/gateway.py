import sqlite3,json,hashlib
OPS={'draft':(), 'send_reminder':('reminder',), 'complete_checklist':('ticket',),'sync_onboarding':('ticket','access_request'),'set_salary':('salary',)}
REVIEWERS={'H1','H2'} # trusted simulated identities; not real authenticated people

def init(db):
    db.executescript('CREATE TABLE IF NOT EXISTS records(id TEXT, field TEXT, value TEXT, PRIMARY KEY(id,field)); CREATE TABLE IF NOT EXISTS receipts(id TEXT PRIMARY KEY,digest TEXT); CREATE TABLE IF NOT EXISTS audit(id TEXT, decision TEXT, reason TEXT);')
    db.executemany('INSERT OR IGNORE INTO records VALUES (?,?,?)',[(i,k,'initial') for i in ('E100','E200') for k in ('reminder','ticket','access_request','salary')]);db.commit()

def decision(t,p):
    if not t['audit'] or t['kill']:return 'BLOCK','infrastructure stop'
    if t['tier'] not in (1,2,3,4):return 'BLOCK','unknown tier'
    if not isinstance(p,dict) or set(p)!={'operation','record_id','value'}:return 'BLOCK','invalid schema'
    if type(p['operation']) is not str or p['operation'] not in OPS or type(p['record_id']) is not str:return 'BLOCK','invalid operation or target'
    if p['operation']!=t['operation'] or p['record_id']!=t['record_id'] or type(p['value']) is not type(t['value']) or p['value']!=t['value']:return 'BLOCK','mandate mismatch'
    if not t['owner'] or not t['scope'] or t['anomaly']:return 'ESCALATE','owner/scope/anomaly'
    op=p['operation']; approvals=set(t['approval_ids']) & REVIEWERS
    if op=='draft':return 'ALLOW','authorized draft'
    if t['tier']==4 or op=='set_salary':return ('ALLOW','dual trusted approvals') if len(approvals)>=2 else ('ESCALATE','dual approval required')
    if t['tier']==1:return ('ALLOW','trusted approval') if approvals else ('ESCALATE','human review required')
    if t['tier']==2 and len(OPS[op])>1:return 'ESCALATE','cross-system outside bounded tier'
    if t['tier']==3 and not(t['risk'] and t['eval'] and t['rollback']):return 'ESCALATE','delegation prerequisite missing'
    return 'ALLOW','within authority'

def execute(db,c,p):
    t=c['trusted']; cid=c['id']; d,reason=decision(t,p)
    # Trusted context is supplied by the application, never by the model.
    if d=='ALLOW' and OPS[p['operation']]:
        digest=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()
        try:
            with db:
                prev=db.execute('SELECT digest FROM receipts WHERE id=?',(cid,)).fetchone()
                if prev:
                    d,reason=('REPLAY','already committed') if prev[0]==digest else ('BLOCK','conflicting replay')
                else:
                    for j,k in enumerate(OPS[p['operation']]):
                        cur=db.execute('UPDATE records SET value=? WHERE id=? AND field=?',(str(p['value']),p['record_id'],k))
                        if cur.rowcount!=1:raise RuntimeError('record missing')
                        if j==0 and t['fault']:raise RuntimeError('injected fault')
                    db.execute('INSERT INTO receipts VALUES (?,?)',(cid,digest))
        except RuntimeError:d,reason='ROLLBACK','transaction rolled back'
    # Local lab audit, separate from simulated external audit availability.
    db.execute('INSERT INTO audit VALUES (?,?,?)',(cid,d,reason));db.commit();return d,reason

"""Post-hoc matched ablation, not preregistered; uses prior experiment fixtures."""
import sys, json, csv
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'governance_comparative'))
import experiment as e
original=e.decide
cases=json.loads((e.ROOT/'main_run/cases.json').read_text()); proposals=json.loads((e.ROOT/'main_run/proposals.json').read_text())
# Keep all baseline infrastructure and oracle definitions. Tier-only removes just the mandate comparison.
import inspect
src=inspect.getsource(original).replace('def decide(', 'def tier_only(').replace("if op!=s['intended']: return 'BLOCK',False,'outside trusted operation mandate'",'if False: pass')
ns=vars(e).copy(); exec(src,ns); tier_only=ns['tier_only']
def mandate_only(group,s,p,err):
    d,r,why=original('A',s,p,err)
    if d=='ALLOW' and p['operation']!=s['intended']:return 'BLOCK',False,'outside trusted operation mandate'
    return d,r,why
rows=[]
for label,fn in [('neither',lambda g,s,p,r:original('A',s,p,r)),('mandate_only',mandate_only),('tiers_only',tier_only),('both',original)]:
    e.decide=lambda g,s,p,r:fn(g,s,p,r) if g=='C' else original(g,s,p,r)
    summary=e.execute(cases,proposals,.02,ROOT/('ablation_'+label))['C']; rows.append({'variant':label,**summary})
with (ROOT/'ablation.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(rows,indent=2))

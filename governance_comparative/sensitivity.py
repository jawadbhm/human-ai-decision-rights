"""Run preselected stress settings; preserve same case mix, task random draws, and seed."""
from experiment import ROOT,make_cases,synthetic_proposal,execute,writecsv
import json
settings=[('low_model_error',.01,.25,.01),('main',.05,.65,.02),('high_model_error',.15,.85,.05),('fallible_human',.05,.65,.10),('perfect_human',.05,.65,0.0)]
root=ROOT/'sensitivity';root.mkdir(exist_ok=True);cases=make_cases(1000,20261127);rows=[]
for label,error,attack,review in settings:
    if label=='main': summary=json.loads((ROOT/'main_run'/'summary.json').read_text())
    else: summary=execute(cases,{s['id']:synthetic_proposal(s,error,attack) for s in cases},review,root/label)
    for arm,metrics in summary.items(): rows.append({'setting':label,'proposal_error':error,'injection_follow':attack,'human_review_error':review,'arm':arm,**metrics})
writecsv(root/'sensitivity.csv',rows)
print('\n'.join(f"{r['setting']:19} {r['arm']} unsafe={r['unauthorized_writes']:3} reviews={r['human_reviews']:3} correct={r['correct_outcome_pct']:.1f}%" for r in rows))

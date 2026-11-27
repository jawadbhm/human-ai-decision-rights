import json, sys
from pathlib import Path
root = Path(__file__).resolve().parent
main, v2 = [json.loads(Path(p).read_text()) for p in sys.argv[1:3]]
expected = json.loads((root/'governance_comparative/main_run/summary.json').read_text())
for arm in 'ABC':
    for metric in expected[arm]:
        assert abs(main[arm][metric]-expected[arm][metric]) < 1e-8, (arm,metric)
assert v2 == json.loads((root/'data/v2_summary.json').read_text())
print('All recorded summary metrics reproduced; 48/48 fixture outcomes reproduced.')

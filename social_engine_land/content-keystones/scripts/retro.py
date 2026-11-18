"""Weekly retro. python3 scripts/retro.py <week>
Ranks posts by PROOF starts per 1,000 views and compares each A/B test."""
import sys, os, csv
sys.path.insert(0, os.path.dirname(__file__))
from ks_social import ROOT
week = sys.argv[1]
rows = list(csv.DictReader(open(os.path.join(ROOT, "06_results", week + ".csv"))))
def num(x):
    try: return float(x)
    except: return 0.0
for r in rows:
    v = num(r["views"]); r["rate"] = num(r["proof_starts"]) * 1000 / v if v else 0
rows.sort(key=lambda r: -r["rate"])
print("Ranked by PROOF starts per 1,000 views")
for r in rows: print(f"  {r['id']:7} {r['channel']:8} {r['hook']:5} {r['rate']:6.2f}  views {r['views'] or '-'}")
tests = {}
for r in rows:
    if r["test"]:
        name, arm = (r["test"].split(":", 1) + [""])[:2]
        tests.setdefault(name, {}).setdefault(arm, []).append(r["rate"])
for name, arms in tests.items():
    print(f"\nTest {name}")
    for arm, xs in arms.items(): print(f"  {arm:24} avg {sum(xs)/len(xs):.2f} over {len(xs)} posts")
print("\nWrite at most two rows into _context/learnings.md. Kept rows change the next brief.")

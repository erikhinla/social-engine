"""Record results. python3 scripts/log_results.py <week>
Creates 06_results/<week>.csv with one row per published post, ready to fill from each platform's
analytics. PROOF starts: on the server, grep 'proof' /var/log/nginx/access.log | grep 's=<post id>'."""
import sys, os, csv
sys.path.insert(0, os.path.dirname(__file__))
from ks_social import ROOT, posts, parse_post
week = sys.argv[1]
f = os.path.join(ROOT, "06_results", week + ".csv")
if os.path.exists(f): sys.exit(f"{f} exists; fill it in")
rows = []
for p in posts([os.path.join(ROOT, "04_approved", week), os.path.join(ROOT, "05_published", week)]):
    m, _ = parse_post(p)
    rows.append([m.get("id"), m.get("channel"), m.get("hook"), m.get("test", ""), "", "", "", ""])
with open(f, "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["id", "channel", "hook", "test", "views", "engagements", "link_clicks", "proof_starts"]); w.writerows(rows)
print("wrote", f, len(rows), "rows")

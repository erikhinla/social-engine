"""Start a week: python3 scripts/new_week.py 2026-11-19
Writes 01_briefs/W<n>-<date>.md from templates/brief.md with kept learnings and the channel plan."""
import sys, os, glob
sys.path.insert(0, os.path.dirname(__file__))
from ks_social import ROOT, table, read

start = sys.argv[1]
n = len(glob.glob(os.path.join(ROOT, "01_briefs", "W*.md"))) + 1
week = f"W{n}-{start}"
kept = [r for r in table("learnings.md") if r.get("kept?", "").lower().startswith("y")]
learn = "\n".join(f"- {r['what we\'ll do differently']}" for r in kept) or "- none yet"
chans = "\n".join(f"- {r['channel id']}: {r['cadence']} ({r['format that wins there']})" for r in table("channels.md")
                  if r.get("cadence") and r["cadence"] != "0")
t = read(os.path.join(ROOT, "templates", "brief.md"))
t = t.replace("{{WEEK}}", week).replace("{{START}}", start).replace("{{LEARNINGS}}", learn).replace("{{CHANNELS}}", chans)
out = os.path.join(ROOT, "01_briefs", week + ".md")
if os.path.exists(out):
    sys.exit(f"{out} already exists")
open(out, "w").write(t)
os.makedirs(os.path.join(ROOT, "02_drafts", week), exist_ok=True)
print("wrote", out)

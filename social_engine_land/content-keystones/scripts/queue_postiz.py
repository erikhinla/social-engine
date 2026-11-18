"""Round R3: turn approved posts into Postiz draft payloads. It never schedules.
Usage: python3 scripts/queue_postiz.py <week>
Writes 03_review/<week>/postiz-drafts.json. The social engine or the Postiz connector creates
them as drafts; Erik presses schedule in Postiz."""
import sys, os, json, datetime
sys.path.insert(0, os.path.dirname(__file__))
from ks_social import ROOT, posts, parse_post
from check_post import check, table

# Postiz integration ids, from the Postiz integration list on 2026-11-18.
POSTIZ = {"x-tbtx": "cmuxokigo005is377f0ucreew", "x-erik": "cmukhdwft000boe7fxscn32o5",
          "li-erik": "cmucu0oe30009oe7fcvbtabui", "li-tbtx": "cmuctmqgc0003oe7ffgfaejet",
          "ig-erik": "cmukr21mu0001s3778drk6kdu", "yt-erik": "cmukke4cr000doe7fsax5p1nv",
          "fb-tbtx": "cmuktbrdw0003s37725b1ysvp"}

week = sys.argv[1]
channels = {r["channel id"]: r for r in table("channels.md") if r.get("channel id")}
hooks = {r["id"]: r for r in table("hooks.md")}
rights = {r["asset"]: r for r in table("rights-and-licenses.md")}
out, skipped = [], []
for p in posts([os.path.join(ROOT, "04_approved", week), os.path.join(ROOT, "02_drafts", week)]):
    meta, n, res = check(p, channels, hooks, rights)
    why = None
    if meta.get("status") != "approved": why = "not approved"
    elif any(s == "FAIL" for s, _ in res): why = "fails R1"
    elif meta.get("channel") not in POSTIZ: why = "no Postiz channel"
    elif datetime.date.fromisoformat(meta["date"]) < datetime.date.today(): why = "date has passed"
    if why:
        skipped.append((meta.get("id"), why)); continue
    _, body = parse_post(p)
    out.append({"post_id": meta["id"], "integration": POSTIZ[meta["channel"]], "type": "draft",
                "date": f"{meta['date']}T{meta.get('time','13:00')}:00", "content": body,
                "first_comment": meta.get("reply", ""), "media": meta.get("asset", "")})
d = os.path.join(ROOT, "03_review", week); os.makedirs(d, exist_ok=True)
json.dump(out, open(os.path.join(d, "postiz-drafts.json"), "w"), indent=2)
print(f"{len(out)} drafts ready, {len(skipped)} held")
for i, w in skipped: print(f"  held {i}: {w}")

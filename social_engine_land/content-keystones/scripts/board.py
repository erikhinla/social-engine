"""Round R2: render the review board Erik approves from.
Usage: python3 scripts/board.py <week> [--out DIR]
Writes 03_review/<week>/board.html (and copies the images beside it)."""
import sys, os, re, html, shutil
sys.path.insert(0, os.path.dirname(__file__))
from ks_social import ROOT, posts, parse_post, read, table
from check_post import check

week = sys.argv[1]
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "03_review", week)
os.makedirs(os.path.join(out, "img"), exist_ok=True)
src = os.path.join(ROOT, "02_drafts", week)
for f in os.listdir(os.path.join(src, "img")) if os.path.isdir(os.path.join(src, "img")) else []:
    if not f.endswith("-clean.png"):
        shutil.copy2(os.path.join(src, "img", f), os.path.join(out, "img", f))
channels = {r["channel id"]: r for r in table("channels.md") if r.get("channel id")}
hooks = {r["id"]: r for r in table("hooks.md")}
rights = {r["asset"]: r for r in table("rights-and-licenses.md")}
NAMES = {"x-tbtx": ("X", "TransformBy10X", "@transformby10x"), "x-erik": ("X", "Erik H Bush", "@ErikHBush"),
         "li-erik": ("LinkedIn", "Erik Howerbush", "personal profile"), "li-tbtx": ("LinkedIn", "TransformBy10X", "company page"),
         "ig-erik": ("Instagram", "Erik H Bush", "feed"), "yt-erik": ("YouTube Shorts", "Erik H Bush", "channel"),
         "fb-tbtx": ("Facebook", "TransformBy10X", "page")}
brief = read(os.path.join(ROOT, "01_briefs", week + ".md"))
idea = re.search(r"## The idea this week\n(.*?)\n## ", brief, re.S).group(1).strip()
tests = re.search(r"## Tests\n(.*?)(\n## |\Z)", brief, re.S).group(1).strip()
E = html.escape

def media(meta):
    a, out_ = meta.get("asset", ""), ""
    for x in [s.strip() for s in a.split(",") if s.strip()]:
        k, _, ref = x.partition(":")
        if k == "reel":
            out_ += f'<video src="img/{ref}-reel.mp4" muted loop autoplay playsinline poster="img/W1-02-1-v.png" class="reel"></video>'
            break
        if k == "render":
            imgs = sorted(f for f in os.listdir(os.path.join(out, "img")) if re.fullmatch(rf"{ref}-\d+\.png", f))
            if meta["channel"] in ("ig-erik", "yt-erik") and meta.get("test", "").endswith("reel"):
                continue
            cls = "car" if len(imgs) > 1 else "one"
            out_ += f'<div class="{cls}">' + "".join(f'<img src="img/{f}" loading="lazy" alt="">' for f in imgs) + "</div>"
    return out_

cards = []
for p in posts([src]):
    meta, n, res = check(p, channels, hooks, rights)
    _, body = parse_post(p)
    plat, name, handle = NAMES.get(meta["channel"], ("?", "?", "?"))
    flags = "".join(f'<li class="{s.lower()}">{E(m)}</li>' for s, m in res)
    reply = f'<div class="reply"><span>{"First comment" if meta["channel"].startswith("li") else "First reply"}</span>{E(meta["reply"])}</div>' if meta.get("reply") else ""
    hk = hooks.get(meta.get("hook"), {})
    cards.append(f'''<article class="post {meta["channel"]}"><header><b>{E(plat)}</b><span>{E(meta["date"])} · {E(meta.get("time",""))}</span></header>
<div class="who"><i>{E(name[:1])}</i><div><b>{E(name)}</b><small>{E(handle)}</small></div></div>
<div class="tx">{E(body)}</div>{media(meta)}{reply}
<footer><span>{E(meta["id"])} · hook {E(meta.get("hook",""))} ({E(hk.get("status",""))})</span><span>{n} chars{" · test " + E(meta["test"]) if meta.get("test") else ""}</span></footer>
{f'<ul class="flags">{flags}</ul>' if flags else '<ul class="flags"><li class="pass">Passes every house rule</li></ul>'}</article>''')

page = f'''<title>TBTX Content {E(week)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: the week's posts as they'd appear, on the proof sheet. Single light look on purpose, matching the brand. */
:root{{--ink:#0B0B0C;--paper:#F6F6F2;--card:#fff;--rule:#dcdbd3;--dim:#6b6a64;--mg:#D01E98;--ok:#1f7a4d;--warn:#a26200;color-scheme:light}}
body{{background:var(--paper);color:var(--ink);font-family:"Inter Tight",Arial,sans-serif;font-size:15px;line-height:1.45;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.wrap{{max-width:1320px;margin:0 auto;padding-block:48px 96px;display:grid;gap:48px}}
.mono{{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase}}
h1{{font-size:clamp(36px,5vw,64px);font-weight:800;letter-spacing:-.035em;line-height:.98;margin:10px 0 0;text-wrap:balance}}
h2{{font-size:28px;font-weight:800;letter-spacing:-.02em;margin:0 0 14px}}
p{{margin:0;max-width:72ch}}
.top{{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:40px;align-items:end}}
.top .idea{{font-size:18px;margin-top:18px}}
.tests{{border-top:2px solid var(--ink);padding-top:14px;white-space:pre-line;font-size:14px;color:var(--dim)}}
.grid{{columns:3 380px;column-gap:20px}}
.post{{break-inside:avoid;background:var(--card);border:1px solid var(--rule);margin:0 0 20px;display:flex;flex-direction:column}}
.post header{{display:flex;justify-content:space-between;padding:10px 14px;border-bottom:1px solid var(--rule);font-family:"IBM Plex Mono",monospace;font-size:12px}}
.post header b{{font-weight:500;color:var(--mg);text-transform:uppercase;letter-spacing:.08em}}
.who{{display:flex;gap:10px;align-items:center;padding:12px 14px 0}}
.who i{{width:34px;height:34px;border-radius:50%;background:var(--ink);color:var(--paper);display:grid;place-items:center;font-style:normal;font-weight:700}}
.who b{{display:block;font-size:15px}}.who small{{color:var(--dim)}}
.tx{{padding:10px 14px 12px;white-space:pre-line;font-size:15.5px;overflow-wrap:anywhere}}
.one img,.reel{{display:block;width:calc(100% - 28px);margin:0 14px 12px;border:1px solid var(--rule)}}
.reel{{aspect-ratio:9/16;object-fit:cover;background:#000}}
.car{{display:flex;gap:8px;overflow-x:auto;padding:0 14px 12px;scroll-snap-type:x mandatory}}
.car img{{width:78%;flex:none;border:1px solid var(--rule);scroll-snap-align:start}}
.reply{{margin:0 14px 12px;padding:10px 12px;background:var(--paper);font-size:14px;overflow-wrap:anywhere}}
.reply span{{display:block;font-family:"IBM Plex Mono",monospace;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--dim);margin-bottom:4px}}
.post footer{{margin-top:auto;display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;padding:9px 14px;border-top:1px solid var(--rule);font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--dim)}}
.flags{{list-style:none;margin:0;padding:8px 14px 12px;font-size:13px;display:grid;gap:4px}}
.flags li::before{{content:"";display:inline-block;width:8px;height:8px;margin-right:8px;vertical-align:middle}}
.flags .pass{{color:var(--ok)}}.flags .pass::before{{background:var(--ok)}}
.flags .warn{{color:var(--warn)}}.flags .warn::before{{background:var(--warn)}}
.flags .fail{{color:#b00020}}.flags .fail::before{{background:#b00020}}
.ask{{border-top:2px solid var(--ink);padding-top:20px;display:grid;gap:10px}}
@media (max-width:800px){{.top{{grid-template-columns:1fr}}}}
</style>
<div class="wrap">
<section class="top"><div><div class="mono">TransformBy10X · content · {E(week)} · drafts for your approval</div><h1>AI created a job. Nobody applied.</h1><p class="idea">{E(idea)}</p></div>
<div class="tests"><div class="mono" style="color:var(--ink);margin-bottom:6px">What this week tests</div>{E(tests)}</div></section>
<section><h2>{len(cards)} posts across 7 channels</h2><div class="grid">{"".join(cards)}</div></section>
<section class="ask"><h2>Your call</h2><p>Approve all, approve by number (for example "approve W1-01 to W1-08"), or give notes on any post. Approved posts go to Postiz as drafts. You press schedule. Nothing posts on its own.</p></section>
</div>'''
open(os.path.join(out, "board.html"), "w").write(page)
print("wrote", os.path.join(out, "board.html"), len(cards), "posts")

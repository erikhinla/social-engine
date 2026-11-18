"""Round R1: check posts against the house rules in _context/.
Usage: python3 scripts/check_post.py <file or folder> [...]
Exit code 1 if anything FAILS."""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ks_social import parse_post, table, posts, read, CTX

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⭕]")
BANNED = ["synergy", "leverage", "unlock", "revolutionize", "game-changer", "game changer", "supercharge",
          "digital fog", "flow agent", "mr. nobody", "bizbuilders"]
LIMITS = {"x-tbtx": 280, "x-erik": 280, "li-erik": 3000, "li-tbtx": 3000, "ig-erik": 2200, "yt-erik": 5000, "fb-tbtx": 5000}
LINK_HOSTS = ("transformby10x.ai", "erikhbush.com")


def chars_for_x(body):
    # X counts every link as 23 characters.
    return len(re.sub(r"https?://\S+", "x" * 23, body))


def check(path, channels, hooks, rights):
    meta, body = parse_post(path)
    res = []
    def fail(m): res.append(("FAIL", m))
    def warn(m): res.append(("WARN", m))
    text = body + "\n" + meta.get("reply", "") + "\n" + "\n".join(meta.get("cards", []) if isinstance(meta.get("cards"), list) else [meta.get("cards", "")])
    low = text.lower()
    for k in ("id", "channel", "date", "hook", "status"):
        if not meta.get(k):
            fail(f"front matter is missing {k}")
    ch = meta.get("channel", "")
    if ch and ch not in channels:
        fail(f"unknown channel {ch}")
    if ch == "x-seraphina":
        fail("x-seraphina has no content until Erik decides what it is")
    if "—" in text or "–" in text:
        fail("em or en dash")
    if EMOJI.search(text):
        fail("emoji")
    for w in BANNED:
        if w in low:
            fail(f"banned word: {w}")
    if re.search(r"fact[^.\n]{0,40}\$\d", low) or re.search(r"\$\d[^.\n]{0,40}\bfact\b", low):
        fail("FACT price")
    if "back" in low and re.search(r"\bfact\b", low) and "transformby10x.ai/back" in low:
        fail("a BACK post mentions FACT")
    h = hooks.get(meta.get("hook", ""))
    if meta.get("hook") and not h:
        fail(f"hook {meta.get('hook')} is not in hooks.md")
    elif h and h["status"] == "retired":
        fail(f"retired hook {meta['hook']}")
    elif h and h["status"] == "new":
        warn(f"hook {meta['hook']} is new and needs Erik's yes")
    if "3-day" in low or "three-day" in low:
        fail("3-day turnaround hook is retired")
    if "OPEN:" in text:
        fail("unanswered OPEN: question")
    links = re.findall(r"https?://\S+|(?<![\w/])(?:transformby10x\.ai|erikhbush\.com)\S*", body + "\n" + meta.get("reply", ""))
    body_links = re.findall(r"https?://\S+", body)
    ours = [l for l in links if any(hh in l for hh in LINK_HOSTS)]
    if links and not ours:
        fail("links to a site that isn't ours")
    for l in ours:
        if "?s=" not in l and "transformby10x.ai" in l:
            fail(f"link without tracking tag: {l} (add ?s={meta.get('id','<id>')})")
        elif "?s=" in l and meta.get("id") and f"?s={meta['id']}" not in l:
            fail(f"tracking tag doesn't match post id: {l}")
    rule = channels.get(ch, {}).get("link", "").lower()
    if ch.startswith("x-") and body_links:
        warn("X link in the post body. channels.md says first reply; put it under 'reply:' unless this is the A/B test")
    if ch == "li-erik" and body_links:
        fail("LinkedIn personal: no outside link in the post body, use first comment")
    if ch == "ig-erik" and body_links:
        warn("Instagram doesn't make caption links clickable; say 'link in bio'")
    lim = LIMITS.get(ch)
    n = chars_for_x(body) if ch.startswith("x-") else len(body)
    if lim and n > lim:
        fail(f"{n} characters, limit {lim}")
    a = meta.get("asset", "")
    for asset in [x.strip() for x in a.split(",") if x.strip()]:
        r = rights.get(asset)
        if r is None:
            if not asset.startswith(("render:", "reel:")):
                warn(f"asset {asset} isn't listed in rights-and-licenses.md")
        else:
            cl = r["cleared for"].lower()
            if cl in ("none", "open") or (cl != "all" and not (cl == "founder channels" and ch.endswith("erik"))):
                fail(f"asset {asset} not cleared for {ch} ({r['cleared for']})")
    return meta, n, res


def main(args):
    channels = {r["channel id"]: r for r in table("channels.md") if r.get("channel id")}
    hooks = {r["id"]: r for r in table("hooks.md")}
    rights = {r["asset"]: r for r in table("rights-and-licenses.md")}
    bad = 0
    files = posts(args)
    for p in files:
        meta, n, res = check(p, channels, hooks, rights)
        fails = [m for s, m in res if s == "FAIL"]
        bad += bool(fails)
        tag = "FAIL" if fails else ("WARN" if res else "PASS")
        print(f"{tag:4}  {meta.get('id','?'):7} {meta.get('channel','?'):8} {n:5} chars  {os.path.basename(p)}")
        for s, m in res:
            print(f"        {s}: {m}")
    print(f"\n{len(files)} posts, {bad} failing")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["02_drafts"]))

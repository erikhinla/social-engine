"""Shared helpers for the TBTX content pack. Standard library only."""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTX = os.path.join(ROOT, "_context")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_post(path):
    """Return (meta dict, body str) from a post file with --- front matter."""
    t = read(path)
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", t, re.S)
    if not m:
        return {}, t.strip()
    meta, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\s+- ", line) and key:
            meta.setdefault(key, [])
            if not isinstance(meta[key], list):
                meta[key] = [meta[key]] if meta[key] else []
            meta[key].append(line.strip()[2:].strip())
            continue
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if kv:
            key = kv.group(1)
            v = kv.group(2).strip().strip('"')
            meta[key] = v
    return meta, m.group(2).strip()


def table(name):
    """Rows of a pipe table in a _context file, as dicts keyed by the header."""
    rows, head = [], None
    for line in read(os.path.join(CTX, name)).splitlines():
        if "|" not in line or set(line.replace("|", "").strip()) <= set("-: "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if head is None:
            head = [c.lower() for c in cells]
            continue
        rows.append(dict(zip(head, cells)))
    return rows


def posts(paths):
    out = []
    for p in paths:
        p = p if os.path.isabs(p) else os.path.join(os.getcwd(), p)
        if os.path.isdir(p):
            out += sorted(glob.glob(os.path.join(p, "**", "*.md"), recursive=True))
        elif p.endswith(".md"):
            out.append(p)
    return [p for p in out if not os.path.basename(p).startswith(("BRIEF", "NOTES"))]


def week_dir(week, stage="02_drafts"):
    return os.path.join(ROOT, stage, week)

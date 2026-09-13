#!/usr/bin/env python3
"""Create blobs/tree/commit on GitHub via `gh api`. No local clone."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = "erikhinla/hermes-agent"
BRANCH = "social-asset-pipeline/init"
EXPECTED_SHA = "a3ef441cda9cb3bf8ec9ee07cd23c80a01f638bf"
ROOT = Path(__file__).resolve().parent

FILES = [
    "SOCIAL_ENGINE.md",
    "social_engine/README.md",
    "social_engine/requirements.txt",
    "social_engine/.env.example",
    "social_engine/pytest.ini",
    "social_engine/app/__init__.py",
    "social_engine/app/main.py",
    "social_engine/app/db.py",
    "social_engine/app/models.py",
    "social_engine/app/clients.py",
    "social_engine/app/verify.py",
    "social_engine/app/pipeline.py",
    "social_engine/app/prompts.py",
    "social_engine/app/config.py",
    "social_engine/tests/test_pipeline.py",
    "social_engine/tests/conftest.py",
]


def gh_api(method: str, path: str, payload: dict | None = None) -> dict:
    cmd = ["gh", "api", "--method", method, path]
    if payload is not None:
        cmd.extend(["--input", "-"])
    proc = subprocess.run(
        cmd,
        input=json.dumps(payload) if payload is not None else None,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"gh api {method} {path} failed:\n{proc.stderr}\n{proc.stdout}")
    return json.loads(proc.stdout) if proc.stdout.strip() else {}


def main() -> None:
    ref = gh_api("GET", f"repos/{REPO}/git/ref/heads/{BRANCH}")
    current_sha = ref["object"]["sha"]
    print("current ref sha", current_sha)
    if current_sha != EXPECTED_SHA:
        raise SystemExit(
            f"abort: branch moved. expected {EXPECTED_SHA}, got {current_sha}. no force."
        )
    commit = gh_api("GET", f"repos/{REPO}/git/commits/{current_sha}")
    base_tree = commit["tree"]["sha"]
    print("base tree", base_tree)

    tree_entries = []
    for rel in FILES:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"missing file {path}")
        content = path.read_text(encoding="utf-8")
        blob = gh_api(
            "POST",
            f"repos/{REPO}/git/blobs",
            {"content": content, "encoding": "utf-8"},
        )
        print("blob", rel, blob["sha"])
        tree_entries.append(
            {"path": rel, "mode": "100644", "type": "blob", "sha": blob["sha"]}
        )

    tree = gh_api(
        "POST",
        f"repos/{REPO}/git/trees",
        {"base_tree": base_tree, "tree": tree_entries},
    )
    print("new tree", tree["sha"])

    message = "\n".join(
        [
            "Add TBTX social asset pipeline engine",
            "",
            "Self-contained FastAPI package under social_engine/. Copy, Telegram",
            "approval, Venice stills, pixel verify, then Postiz drafts only.",
        ]
    )
    new_commit = gh_api(
        "POST",
        f"repos/{REPO}/git/commits",
        {
            "message": message,
            "tree": tree["sha"],
            "parents": [current_sha],
        },
    )
    new_sha = new_commit["sha"]
    print("new commit", new_sha)

    updated = gh_api(
        "PATCH",
        f"repos/{REPO}/git/refs/heads/{BRANCH}",
        {"sha": new_sha, "force": False},
    )
    print("updated ref", updated.get("object", {}).get("sha", updated))
    Path("/tmp/social_engine_commit_sha.txt").write_text(new_sha + "\n")


if __name__ == "__main__":
    main()

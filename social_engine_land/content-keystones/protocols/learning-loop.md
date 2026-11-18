# Learning loop: how the skill improves and stays improved

1. Each brief names up to three tests (for example: link in post vs first reply).
2. `05_published/log.csv` records every post with its id, channel and link tag.
3. `06_results/<week>.csv` records views, engagements, clicks and PROOF starts per post. PROOF starts come from the `?s=` tag in the server log.
4. `scripts/retro.py` compares the tests and proposes learnings.
5. Kept learnings go to `_context/learnings.md`. Ones that change a rule go through the change protocol into `brand.md`, `channels.md` or `hooks.md`.
6. When a skill file gets something wrong twice, the skill file changes. The fix lives in the file, not in anyone's head.

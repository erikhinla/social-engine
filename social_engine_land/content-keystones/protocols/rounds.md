# Rounds: who approves what

| Round | Who | What they check | Moves to |
|---|---|---|---|
| R1 Check | scripts/check_post.py, then the writer | House rules, links, rights, length | stays in 02_drafts until green |
| R2 Erik | Erik, on the review board from `scripts/board.py` | Is it good, is it true, is it us | approved posts get `status: approved` and move to 04_approved |
| R3 Queue | scripts/queue_postiz.py | Approved, still green, link tagged, date in the future | Postiz drafts. Erik presses schedule. |

- Erik reviews in layout only: the board, never the markdown.
- A note from Erik becomes a row in `decisions.md` if it applies beyond one post, and a change in `hooks.md` or `brand.md` if it changes a rule.
- Changing an approved post sends it back to R1.

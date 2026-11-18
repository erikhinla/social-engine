# TBTX content: start here

This folder runs TransformBy10X social the same way BACK runs a client's work. The facts live in `_context/`, the work moves through numbered folders, the skills say how each job is done, the protocols say who decides, and the scripts do the checking.

If we sell a workflow that keeps context with the work, our own content has to run on one.

## The loop, once a week

1. **Brief.** `python3 scripts/new_week.py 2026-11-19` creates `01_briefs/W1-2026-11-19.md` and an empty draft folder.
2. **Draft.** Write one file per post in `02_drafts/<week>/`, following `skills/write-a-post.md`. One idea, cut per channel.
3. **Check (R1).** `python3 scripts/check_post.py 02_drafts/<week>` runs the house rules. Nothing goes to Erik with a red line.
4. **Review (R2).** `python3 scripts/board.py <week>` renders the review board. Erik approves in layout, never in a text file.
5. **Queue (R3).** `python3 scripts/queue_postiz.py <week>` writes Postiz drafts for approved posts only. Nothing schedules itself.
6. **Learn.** `python3 scripts/log_results.py` and `python3 scripts/retro.py <week>` turn the numbers into a change in `_context/learnings.md`. The next brief reads it.

## Where things live

| Folder | What goes in it |
|---|---|
| `_context/` | The Keystone files. Every person and every AI reads these first. |
| `01_briefs/` | One brief per week: the idea, the hook, the channels, the goal. |
| `02_drafts/` | Posts being written, one markdown file each. |
| `03_review/` | Review boards and Erik's notes per round. |
| `04_approved/` | Approved posts, moved here by the round. |
| `05_published/` | What went out, with the link and the tracking tag. |
| `06_results/` | Weekly numbers per post. |
| `_archive/` | Older versions. Nothing is deleted. |
| `skills/` | How to do each job, for a person or an AI. |
| `protocols/` | Who decides, and what happens when something changes. |
| `scripts/` | The checks and the plumbing. |

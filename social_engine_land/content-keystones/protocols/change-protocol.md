# Change protocol

When a fact changes (a price, a link, a line, a rule):

1. Update the Keystone file it belongs in. Move the old value to Previous.
2. Add a row to `_context/change-log.md` naming what it affects.
3. Run `python3 scripts/check_post.py 02_drafts 04_approved`. Anything the change breaks shows up red.
4. Fix or pull those posts. A queued Postiz draft that's affected gets deleted in Postiz by Erik and re-queued.

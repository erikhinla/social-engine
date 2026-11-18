# Skill: check a post (round R1)

The script does most of it: `python3 scripts/check_post.py 02_drafts/<week>`.

It fails a post for: an em dash, an emoji, a FACT price, BACK and FACT in the same post, a retired hook, a banned word, a missing or wrong link, a link missing its `?s=` tag, an X post over 280 characters, an asset not cleared for the channel, an unanswered `OPEN:`.

What the script can't judge, a person or an AI checks by hand:
- Does the hook pass the hook test in `brand.md`?
- Would the person in the scene feel seen, not blamed?
- Is every number either from `legal-lines.md` or clearly a scene detail?
Report only. Don't rewrite creative. Erik decides.

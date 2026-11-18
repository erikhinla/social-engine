# Skill: make a proof-sheet still or carousel

1. Pick a layout (defined in `scripts/render.mjs`): `job` (title | line | three duties split by ; | stamp), `cover` (line | marked line), `diptych` (adopted | didn't), `statement` (line | marked line), `end` (headline | sub).
2. Write the card's words in the post file under `cards:`, one card per line, fields split by ` | `.
3. Run `node scripts/render.mjs 02_drafts/<week>`. It writes PNGs to the week's `img/` at 1080x1350 (feed) and 1080x1920 (vertical), plus a stamp-free vertical for reels.
4. For a reel: `sh scripts/reel.sh img/<id>-reel.mp4 <clean frame>:3.2 <stamped frame>:2.6 <end frame>:2.6`. Silent by design (see rights-and-licenses.md).
5. Look at the PNG. Ink headline, one magenta mark, nothing touching the crop marks.

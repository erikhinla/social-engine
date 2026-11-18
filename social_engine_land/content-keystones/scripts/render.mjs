// Render proof-sheet cards for every post in a week folder that has `cards:`.
// Usage: node scripts/render.mjs 02_drafts/<week>
// Needs playwright-core (or playwright) on NODE_PATH and a Chrome/Chromium (CHROME env var or default path).
import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
let pw; try { pw = require('playwright-core'); } catch { pw = require('playwright'); }
const dir = path.resolve(process.argv[2]); const out = path.join(dir, 'img'); fs.mkdirSync(out, { recursive: true });
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
const CSS = `
:root{--ink:#0B0B0C;--paper:#F6F6F2;--mg:#D01E98;--rule:#d9d8d0}
*{box-sizing:border-box;margin:0}
body{width:1080px;height:var(--h);background:var(--paper);color:var(--ink);font-family:"Inter Tight",Arial,sans-serif;position:relative;overflow:hidden}
.crop{position:absolute;width:44px;height:44px;border-color:var(--ink);border-style:solid;opacity:.55}
.c1{top:36px;left:36px;border-width:2px 0 0 2px}.c2{top:36px;right:36px;border-width:2px 2px 0 0}
.c3{bottom:36px;left:36px;border-width:0 0 2px 2px}.c4{bottom:36px;right:36px;border-width:0 2px 2px 0}
.lab{position:absolute;top:56px;left:100px;right:100px;display:flex;justify-content:space-between;font:500 22px "IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase}
.foot{position:absolute;bottom:56px;left:100px;right:100px;display:flex;justify-content:space-between;font:500 22px "IBM Plex Mono",monospace;letter-spacing:.04em}
.foot b{font-weight:500;color:var(--mg)}
.pad{position:absolute;inset:150px 100px 150px}
h1{font-weight:800;letter-spacing:-.035em;line-height:.95}
.stamp{position:absolute;color:var(--mg);border:6px double var(--mg);padding:14px 30px;font:800 64px "Inter Tight";letter-spacing:-.01em;text-transform:uppercase;transform:rotate(-9deg);mix-blend-mode:multiply;opacity:.92}
.mark{background:linear-gradient(transparent 62%,rgba(208,30,152,.28) 62%,rgba(208,30,152,.28) 92%,transparent 92%)}
.strike{text-decoration:line-through;text-decoration-color:var(--mg);text-decoration-thickness:8px}
/* job */
.job .k{font:500 26px "IBM Plex Mono";letter-spacing:.1em;text-transform:uppercase;border-bottom:2px solid var(--ink);padding-bottom:18px}
.job h1{font-size:132px;margin-top:40px}
.job .sub{font-size:40px;font-weight:500;margin-top:26px;line-height:1.2}
.job ul{list-style:none;padding:0;margin-top:56px;border-top:1px solid var(--rule)}
.job li{font-size:36px;line-height:1.25;padding:22px 0;border-bottom:1px solid var(--rule);display:grid;grid-template-columns:70px 1fr}
.job li span{font:500 24px "IBM Plex Mono";padding-top:8px}
.job .meta{margin-top:34px;font:500 26px "IBM Plex Mono";display:flex;gap:40px}
/* cover / statement / end */
.cover h1{font-size:118px}.cover h1+h1{margin-top:18px}
.statement h1{font-size:84px;line-height:1.02}
.statement p{font-size:46px;font-weight:600;margin-top:60px}
.end h1{font-size:108px}.end p{font-size:44px;margin-top:40px;font-weight:500}
.end .url{margin-top:70px;font:500 40px "IBM Plex Mono";border-top:2px solid var(--ink);padding-top:28px}
/* diptych */
.dip{display:grid;grid-template-rows:1fr 1fr;height:100%;gap:0}
.dip>div{border-top:2px solid var(--ink);padding-top:28px;position:relative}
.dip .k{font:500 26px "IBM Plex Mono";letter-spacing:.1em;text-transform:uppercase}
.dip p{font-size:66px;font-weight:700;letter-spacing:-.025em;line-height:1.02;margin-top:26px}
.dip .no .k{color:var(--mg)}
.dip .no p{color:var(--ink)}
.v .pad{inset:220px 100px 220px}
`;
function page(card, i, n, id, h) {
  const [layout, ...f] = card.split('|').map(s => s.trim());
  let inner = '';
  if (layout === 'job') {
    const items = f[2].split(';').map((t, k) => `<li><span>0${k+1}</span>${esc(t)}</li>`).join('');
    inner = `<div class="pad job"><div class="k">Job posting · open since AI arrived</div><h1>${esc(f[0])}</h1><p class="sub">${esc(f[1])}</p><ul>${items}</ul><div class="meta"><span>Reports to: nobody</span><span>Pay: none</span></div></div>
      <div class="stamp" style="right:90px;bottom:${h>1500?430:250}px">${esc(f[3])}</div>`;
  } else if (layout === 'cover') {
    inner = `<div class="pad cover" style="display:flex;flex-direction:column;justify-content:center"><h1>${esc(f[0])}</h1><h1><span class="mark">${esc(f[1])}</span></h1></div>`;
  } else if (layout === 'diptych') {
    inner = `<div class="pad"><div class="dip"><div><div class="k">Adopted</div><p>${esc(f[0])}</p></div><div class="no"><div class="k">Didn't</div><p class="strike-none">${esc(f[1])}</p></div></div></div>
      <div class="stamp" style="right:100px;bottom:${h>1500?360:200}px;font-size:46px">Not built</div>`;
  } else if (layout === 'statement') {
    inner = `<div class="pad statement" style="display:flex;flex-direction:column;justify-content:center"><h1>${esc(f[0])}</h1><p><span class="mark">${esc(f[1])}</span></p></div>`;
  } else if (layout === 'end') {
    inner = `<div class="pad end" style="display:flex;flex-direction:column;justify-content:center"><h1>${esc(f[0])}</h1><p>${esc(f[1])}</p><div class="url">transformby10x.ai/proof</div></div>`;
  }
  return `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700;800&family=IBM+Plex+Mono:wght@500&display=swap"><style>${CSS}</style></head>
  <body class="${h>1500?'v':''}" style="--h:${h}px"><i class="crop c1"></i><i class="crop c2"></i><i class="crop c3"></i><i class="crop c4"></i>
  <div class="lab"><span>TransformBy10X · proof sheet</span><span>${esc(id)} · ${i+1}/${n}</span></div>${inner}
  <div class="foot"><span>Infrastructure before intelligence.</span><b>PROOF</b></div></body></html>`;
}
const posts = fs.readdirSync(dir).filter(f => f.endsWith('.md'));
const browser = await pw.chromium.launch({ executablePath: CHROME });
for (const f of posts) {
  const t = fs.readFileSync(path.join(dir, f), 'utf8');
  const fm = (t.match(/^---\n([\s\S]*?)\n---/) || [])[1] || '';
  const id = (fm.match(/^id:\s*(.+)$/m) || [])[1];
  const cards = []; let on = false;
  for (const line of fm.split('\n')) { if (/^cards:/.test(line)) { on = true; continue; } if (on && /^\s+- /.test(line)) cards.push(line.replace(/^\s+- /, '')); else if (on) on = false; }
  if (!cards.length) continue;
  for (const [w, h, sfx] of [[1080, 1350, ''], [1080, 1920, '-v']]) {
    const p = await browser.newPage({ viewport: { width: w, height: h } });
    for (let i = 0; i < cards.length; i++) {
      await p.setContent(page(cards[i], i, cards.length, id, h), { waitUntil: 'load', timeout: 60000 });
      await p.evaluate(() => document.fonts.ready);
      await p.screenshot({ path: path.join(out, `${id}-${i+1}${sfx}.png`) });
      if (sfx && await p.$('.stamp')) { // a clean frame so the reel can stamp it on screen
        await p.addStyleTag({ content: '.stamp{display:none}' });
        await p.screenshot({ path: path.join(out, `${id}-${i+1}${sfx}-clean.png`) });
      }
    }
    await p.close();
  }
  console.log(id, cards.length, 'cards');
}
await browser.close();

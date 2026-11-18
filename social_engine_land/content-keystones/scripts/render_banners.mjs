// Render profile banners in the proof-sheet design. Usage: node scripts/render_banners.mjs profiles/banners
import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const require = createRequire(import.meta.url); let pw; try { pw = require('playwright-core'); } catch { pw = require('playwright'); }
const out = path.resolve(process.argv[2] || 'profiles/banners'); fs.mkdirSync(out, { recursive: true });
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
// size, where the platform puts the avatar (keep text clear of it), and the safe box for text
const SIZES = {
  x:   { w: 1500, h: 500,  align: 'right', safe: [80, 70, 80, 90] },
  li:  { w: 1584, h: 396,  align: 'right', safe: [60, 70, 60, 120] },
  lip: { w: 1128, h: 191,  align: 'right', safe: [30, 50, 30, 50] },
  yt:  { w: 2560, h: 1440, align: 'center', safe: [508, 507, 508, 507] },
  fb:  { w: 1640, h: 624,  align: 'center', safe: [110, 230, 110, 230] },
  rd:  { w: 1920, h: 384,  align: 'center', safe: [70, 260, 70, 260] },
};
const WHO = { erik: 'Erik H Bush · 20 years in agency operations', tbtx: 'TransformBy10X · PROOF · BACK' };
const page = (s, who) => `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@800&family=IBM+Plex+Mono:wght@500&display=swap"><style>
*{margin:0;box-sizing:border-box}body{width:${s.w}px;height:${s.h}px;background:#F6F6F2;color:#0B0B0C;position:relative;overflow:hidden;font-family:"Inter Tight",Arial}
.c{position:absolute;width:${s.h/10}px;height:${s.h/10}px;border:0 solid #0B0B0C;opacity:.5}
.c1{top:${s.h/20}px;left:${s.h/20}px;border-width:2px 0 0 2px}.c2{top:${s.h/20}px;right:${s.h/20}px;border-width:2px 2px 0 0}.c3{bottom:${s.h/20}px;left:${s.h/20}px;border-width:0 0 2px 2px}.c4{bottom:${s.h/20}px;right:${s.h/20}px;border-width:0 2px 2px 0}
.box{position:absolute;top:${s.safe[0]}px;right:${s.safe[1]}px;bottom:${s.safe[2]}px;left:${s.safe[3]}px;display:flex;flex-direction:column;justify-content:center;align-items:${s.align==='right'?'flex-end':'center'};text-align:${s.align}}
h1{font-weight:800;letter-spacing:-.035em;line-height:.98;font-size:var(--fs)}
h1 span{background:linear-gradient(transparent 60%,rgba(208,30,152,.3) 60%,rgba(208,30,152,.3) 92%,transparent 92%)}
p{font:500 var(--ls) "IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase;margin-top:calc(var(--ls)*1.1);display:flex;gap:1.6em}
p b{font-weight:500;color:#D01E98}
</style></head><body><i class="c c1"></i><i class="c c2"></i><i class="c c3"></i><i class="c c4"></i>
<div class="box"><h1>Your team adopted AI.<br>Your infrastructure <span>didn't.</span></h1><p><span>${WHO[who]}</span><b>Infrastructure before intelligence.</b></p></div></body></html>`;
const b = await pw.chromium.launch({ executablePath: CHROME });
for (const who of ['erik', 'tbtx']) for (const [k, s] of Object.entries(SIZES)) {
  const p = await b.newPage({ viewport: { width: s.w, height: s.h } });
  await p.setContent(page(s, who), { waitUntil: 'load', timeout: 60000 }); await p.evaluate(() => document.fonts.ready);
  // fit: grow the headline until the box is full, then back off
  await p.evaluate(() => { const box = document.querySelector('.box'), r = document.documentElement.style; let fs = 10;
    const fits = () => box.scrollHeight <= box.clientHeight && box.scrollWidth <= box.clientWidth && [...box.children].every(c => c.scrollWidth <= box.clientWidth);
    for (;;) { r.setProperty('--fs', fs + 'px'); r.setProperty('--ls', Math.max(11, fs * .2) + 'px'); if (!fits()) { fs -= 2; break; } fs += 2; }
    r.setProperty('--fs', fs + 'px'); r.setProperty('--ls', Math.max(11, fs * .2) + 'px'); });
  await p.screenshot({ path: path.join(out, `${who}-${k}.png`) }); await p.close();
}
await b.close(); console.log('done');

# HANDOFF.md — Social Engine Session Handoff

**Session:** 2026-09-13  
**Branch:** `handoff/social-engine-2026-09-13`  
**Repo root:** `/Users/test`  
**Working folder:** `/Users/test/social_engine_land`

---

## GOAL

Take a social media engine that currently generates TBTX-brand copy (TransformBy10X, "Start Here" CTA, Mr. Nobody / Managing Digital Fog campaign) and retool it for a new product called **PROOF: Fog & Friction Forensics**. The brand has shifted away from FLOW Agent AS and the old TBTX campaign. PROOF is a Fog & Friction finder tool that lives on `transformby10x.ai/proof` and books meetings with clients via a diagnostic intake (NOT a Calendly link).

The user wants to plan, prep, and post social content. Content types: video/motion/gifs, memes, decks with detailed info, platform-appropriate. Style: premium, engaging, trend-setter in tech — editorial, forensic, cinematic. Not stuffy.

Three concrete sub-tasks were executed this session:
1. Build a content plan document (PROOF_PLAN.md) tying message house, assets, matrix, calendar.
2. Prep assets: render two PDFs to carousel slides, cut a 45-sec vertical brand film.
3. Retool the social engine's prompts for PROOF (CTA, hook language, product name, remove old brand refs).

---

## STATE

### What works (verified)

- **All 8 pytest tests pass** after the prompt rewrite (`.venv/bin/python -m pytest -q` → 8 passed, 8.28s). The rewrite did not break the test suite.
- **Carousel slides rendered** from two PDFs, 2160×2700 (2x retina 4:5 ratio), all verified on disk:
  - `social_engine_land/assets/carousel_forensic/forensic_slide01..12.png` — from `The_Forensic_Instrument.pdf` (12 pages)
  - `social_engine_land/assets/carousel_fog/fog_slide01..06.png` — from `AI_Fog_and_Friction.pdf` (6 pages)
- **45-sec vertical brand film cut**: `social_engine_land/assets/film_cut/proof_brand_45s_vertical.mp4` — 1080×1920, 45.0 sec, H.264, silent (no audio track). Source: `The_Hidden_Human_Repair_Load.mp4` (already 720×1280 vertical, 69.5 sec). Cut from 0:00–0:45, upscaled with lanczos to 1080×1920.
- **Engine prompts fully rewritten** for PROOF in `social_engine/app/prompts.py`: SYSTEM_PROMPT, build_messages, and fake_copy all use PROOF language, CTA is `Map Business Momentum → https://transformby10x.ai/proof`, old brand refs (FLOW Agent AS, Mr. Nobody, BizBuilders, TBTX campaign name) removed or made conditional.
- **CTA model updated** in `social_engine/app/models.py`: `CTA_LINE` and `CTA_URL` changed to the PROOF CTA; `ensure_cta()` recognizes the new CTA string.

### What is half-built (not yet executed)

- **Live Postiz run not done.** The engine is rewired for PROOF but still runs in fake mode (`SOCIAL_ENGINE_FAKE=1`). No real brief has been submitted through the rewired engine to Postiz with live keys. This is the next major step.
- **Sound design on the 45-sec film not done.** The cut is silent. A proper brand film needs audio (directional, pressure, pulse) layered in.
- **Pre-lock archive asset verification not done.** The `SOCIAL_MATRIX.md` points to assets in `99_ARCHIVE/2026-08-19_pre-lock-dump/`. Those paths were not checked for file existence or PROOF-brand fit.
- **PROOF lockup/wordmark not created.** Existing visuals are a mix of PROOF, TBTX, Mr. Nobody, and BizBuilders branding. No consistent PROOF lockup exists yet.
- **The intake experience at `transformby10x.ai/proof` not verified.** Does it exist? Is it diagnostic and not a Calendly link? This was not checked — the CTA points there and the chain is broken if the page doesn't exist.

### What is broken (noted, not fixed)

- Nothing is broken in the code. The engine runs, tests pass, assets render. The gaps are all unbuilt deliverables or unverified decisions, not broken code.

---

## CHANGED

Files created or modified this session, absolute paths:

- `/Users/test/social_engine_land/PROOF_PLAN.md` — **CREATED** (23KB). Full content plan: message house, asset inventory, platform×format×asset matrix, two-week calendar skeleton, engine retool notes, prep checklist, gaps. CTA set to "Map Business Momentum" after the user's correction.
- `/Users/test/social_engine_land/social_engine/app/prompts.py` — **MODIFIED**. SYSTEM_PROMPT rewritten for PROOF. build_messages says "Write a fresh PROOF package". fake_copy fully PROOF-branded (AI multiplied output, human repair load, PROOF one-liner, Map Business Momentum CTA, forensic visual style).
- `/Users/test/social_engine_land/social_engine/app/models.py` — **MODIFIED**. `CTA_LINE` = `Map Business Momentum → https://transformby10x.ai/proof`. `CTA_URL` = `https://transformby10x.ai/proof`. `ensure_cta()` updated to recognize the new CTA string.
- `/Users/test/social_engine_land/assets/` — **CREATED** (directory, not committed to git yet — see RESUME). Contains:
  - `assets/carousel_forensic/forensic_slide01..12.png`
  - `assets/carousel_fog/fog_slide01..06.png`
  - `assets/film_cut/proof_brand_45s_vertical.mp4`

Files read but not modified (for context, not committed):
- Everything under `/Users/test/Library/CloudStorage/GoogleDrive-erikhbush@gmail.com/My Drive/EHB PRODUCTION/` (PROOF campaign assets, editorial decks, videos)
- `/Users/test/Documents/TBTX_COMMAND_CENTER/Campaign elements/05_POSTIZ_PACKAGES/` (Postiz package manifests, queue script)
- `/Users/test/Documents/FLOW BluePrint Visualizer/VISUALIZER_MASTER.md` (product spec for the visualizer)
- `/Users/test/social_engine_land/social_engine/app/*.py` (all engine source read to understand before editing)

---

## RUNNING

- **No long-running process was left running at session close.** The fake-mode uvicorn server (`SOCIAL_ENGINE_FAKE=1`, port 8088) was started during verification and then killed (`pkill -f "uvicorn app.main"`).
- If you need to restart it for testing: `cd /Users/test/social_engine_land/social_engine && SOCIAL_ENGINE_FAKE=1 TELEGRAM_WEBHOOK_SECRET=dev-secret .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8088`
- Stop it with: `pkill -f "uvicorn app.main"` or Ctrl-C in the terminal where it's running.

---

## CONFIG

Environment variables the code needs, by name only. **No secret values are written here.**

| Variable | Used for | Required for |
|---|---|---|
| `XAI_API_KEY` or `GROK_API_KEY` | Grok copy generation (LiveGrokClient) | live copy, not fake mode |
| `OPENROUTER_API_KEY` | Fallback chat completions (LiveGrokClient falls back to OpenRouter if no XAI/GROK key) | live copy via OpenRouter |
| `TELEGRAM_BOT_TOKEN` | Telegram approval messages (LiveTelegramClient) | live Telegram notifications |
| `TELEGRAM_WEBHOOK_SECRET` | Webhook header verification | both fake and live |
| `VENICE_API_KEY` | Venice image generation (LiveVeniceClient) | live image generation |
| `POSTIZ_API_KEY` | Postiz upload + create posts (LivePostizClient) | live Postiz drafts |
| `POSTIZ_API_URL` | Postiz base URL (default `https://api.postiz.com`) | live Postiz |
| `POSTIZ_INTEGRATION_LINKEDIN` | LinkedIn integration ID in Postiz | live LinkedIn posts |
| `POSTIZ_INTEGRATION_X` | X integration ID in Postiz | live X posts |
| `POSTIZ_INTEGRATION_INSTAGRAM` | Instagram integration ID in Postiz | live Instagram posts |
| `POSTIZ_INTEGRATION_FACEBOOK` | Facebook integration ID in Postiz | live Facebook posts |
| `POSTIZ_INTEGRATION_REDDIT` | Reddit integration ID in Postiz | live Reddit posts |
| `POSTIZ_INTEGRATION_YOUTUBE` | YouTube integration ID in Postiz | live YouTube posts |
| `SOCIAL_ENGINE_FAKE` | Set to `1` to use fake clients (no API keys needed) | local dev / testing |
| `SOCIAL_ENGINE_DB` | SQLite DB path (default `social_engine.sqlite`) | both |
| `SOCIAL_ENGINE_PUBLIC_BASE_URL` | Base URL for serving media files if Venice returns raw bytes | live Venice + Postiz fetch |
| `SOCIAL_ENGINE_MEDIA_DIR` | Media storage dir (default `media`) | both |

Fake mode requires only `SOCIAL_ENGINE_FAKE=1` and `TELEGRAM_WEBHOOK_SECRET` (any value). All other keys are optional in fake mode.

---

## DECISIONS

1. **CTA: "Map Business Momentum" over "Map Business Gaps".** User offered both. "Momentum" lands on the Transform side of the MUST arc (the believable lighter Tuesday). "Gaps" sounds like a report/score, which the campaign explicitly avoids ("If the answer is a score or a booking link → DRIFT"). Chose "Map Business Momentum". The hero/sub line stays "See Where Your System Drops Context". Secondary CTA stays "Trace one recurring task from request to done."

2. **CTA URL: `transformby10x.ai/proof`.** From the brief. Not Calendly. Not "Book a Call". The brief explicitly flags "Book a Call" sales traps as drift. The intake must be diagnostic. NOT verified that this page exists — marked UNVERIFIED.

3. **Carousel slide format: 2160×2700 (2x retina 4:5).** LinkedIn carousel standard is 1080×1350 (4:5). Rendering at 2x gives retina-quality slides that downscale cleanly on any display. Source PDFs are image-based (mostly screenshots), so high DPI matters.

4. **Film cut: 1080×1920, 45 sec, silent.** Source (`The_Hidden_Human_Repair_Load.mp4`) is already 720×1280 vertical, 69.5 sec. Cut 0:00–0:45, upscaled with lanczos to 1080×1920. No audio track — sound design is a separate deliverable. The 720×1280 source would also work for social (most platforms accept 720p vertical), but 1080p gives headroom for cropping/re-edit.

5. **Assets commit strategy: generate artifacts NOT committed to git in this session.** The carousel PNGs and film MP4 are in `social_engine_land/assets/` but were not added to git (the session git add focused on source code + PLAN). Reason: they're large binaries (carousel slides are 1-4MB each, film is 7.7MB) and they're generated from source PDFs that ARE in the user's Drive. Re-generating them is straightforward (run the render script). If you want them committed, add `social_engine_land/assets/` to the commit. The render script is at `/tmp/proof_carousel_render.py` and `/tmp/proof_film_cut.py` (not committed — they're throwaway scripts in /tmp).

6. **Engine retool scope: prompts only, not the full pipeline.** Rewrote `prompts.py` (system prompt + build_messages + fake_copy) and `models.py` (CTA constants). Did NOT touch `pipeline.py`, `clients.py`, `main.py`, `db.py`, `verify.py`, or `config.py`. Those are still valid for PROOF — the pipeline logic (brief → copy → approve → assets → Postiz drafts) is generic and doesn't need changes. Only the copy generation layer needed retooling.

7. **Postiz client path: route through the engine's Postiz client, not `queue_postiz_drafts.py`.** The existing `queue_postiz_drafts.py` in `05_POSTIZ_PACKAGES/` is Bluesky-only. The engine's `LivePostizClient` already supports LinkedIn, X, Instagram, Facebook, Reddit, YouTube — which matches the priority ranking in the plan (Priority 1-3). No decision made on extending the Bluesky queue vs. routing through the engine; marked as a decision point for the next session.

---

## BLOCKED

1. **`transformby10x.ai/proof` intake experience — UNVERIFIED.** The CTA points here. Does the page exist? Is it a diagnostic intake and not a Calendly link? This was not checked. The social CTA chain is broken if the page doesn't exist or is a booking link. Blocking the first real post until verified.

2. **Live Postiz run — blocked on API keys.** The engine is rewired for PROOF but runs in fake mode. To go live you need XAI/GROK, TELEGRAM, VENICE, POSTIZ keys + integration IDs from Infisical. These are not available in this session. No real brief has been run through the rewired engine.

3. **45-sec brand film audio — blocked on sound design.** The cut is silent. If you want a proper brand film, audio needs to be added (directional, pressure, pulse per the style bar). This is a creative deliverable, not a file-find.

4. **PROOF lockup/wordmark — blocked on design.** No consistent PROOF lockup exists. Existing visuals are a mix of brands. If every post should carry a PROOF lockup, that's a design asset to create.

5. **Pre-lock archive asset verification — blocked on eyes.** The SOCIAL_MATRIX.md points to assets in `99_ARCHIVE/2026-08-19_pre-lock-dump/`. File existence and PROOF-brand fit not checked. Needs a human to open the files and decide.

6. **Carousel slides from `DECK_Architecting_AI_Flow.pdf` and `The_AI_Shadow_Work_Burden.pdf` — not rendered.** The plan lists these as deep-dive deck sources. Only the two campaign PDFs (`The_Forensic_Instrument.pdf`, `AI_Fog_and_Friction.pdf`) were rendered this session. The editorial PDFs are larger (14-15 pages) and would need a separate render pass.

---

## NEXT

Three actions in order, executable without asking a question:

1. **Verify `transformby10x.ai/proof` exists and is diagnostic (not Calendly).** Open the URL in a browser. If it doesn't exist, create the intake page or redirect. If it's Calendly, replace with the diagnostic. This unblocks the CTA chain.

2. **Run one real brief through the rewired engine to Postiz drafts.** Wire the live keys from Infisical (XAI/GROK, TELEGRAM, VENICE, POSTIZ + integration IDs), set `SOCIAL_ENGINE_FAKE=0`, submit a brief via `POST /briefs`, approve via the Telegram webhook, and confirm the draft lands at `staged` with Postiz post IDs. This validates the full rewired pipeline end-to-end with real services.

3. **Render the editorial PDFs to carousel slides.** Run the same render approach on `DECK_Architecting_AI_Flow.pdf` (15 slides) and `The_AI_Shadow_Work_Burden.pdf` (14 pages) — these are the deep-dive deck sources for LinkedIn carousels. Script pattern is in `/tmp/proof_carousel_render.py` (re-create it from the session or re-author).

---

## RESUME

Exact commands to get back to this point on a fresh machine:

```bash
# 1. Clone / navigate to the repo root
cd /Users/test

# 2. Switch to the handoff branch
git checkout handoff/social-engine-2026-09-13

# 3. Navigate to the social engine
cd social_engine_land/social_engine

# 4. Create venv and install deps (if not already done)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 5. Run tests to confirm the prompt rewrite is intact
.venv/bin/python -m pytest -q

# 6. Start fake-mode server for local testing
cd /Users/test/social_engine_land/social_engine
SOCIAL_ENGINE_FAKE=1 TELEGRAM_WEBHOOK_SECRET=dev-secret .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8088

# 7. Submit a test brief (verify PROOF copy comes back)
curl -sS -X POST http://127.0.0.1:8088/briefs \
  -H 'Content-Type: application/json' \
  -d '{"brief":"test the PROOF retool","telegram_chat_id":"12345"}' | python3 -m json.tool

# 8. The generated assets are in:
#    /Users/test/social_engine_land/assets/carousel_forensic/
#    /Users/test/social_engine_land/assets/carousel_fog/
#    /Users/test/social_engine_land/assets/film_cut/
#    (These were NOT committed to git in this session — see DECISIONS.)
```

To regenerate the carousel slides and film cut (the render scripts were in `/tmp/` and are not committed):

```bash
# Carousel slides (render script pattern — re-author from the session)
python3 -c "
import fitz
from pathlib import Path
from PIL import Image
import io

OUT_FORE = Path('social_engine_land/assets/carousel_forensic')
OUT_FOG = Path('social_engine_land/assets/carousel_fog')
FORE_PDF = 'PATH_TO_The_Forensic_Instrument.pdf'   # from Google Drive
FOG_PDF = 'PATH_TO_AI_Fog_and_Friction.pdf'        # from Google Drive
TW, TH = 2160, 2700

def render(pdf, out, prefix):
    doc = fitz.open(pdf)
    out.mkdir(parents=True, exist_ok=True)
    for i in range(doc.page_count):
        pix = doc[i].get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes('png')))
        sw, sh = img.size
        r = TW / TH
        if sw/sh > r:
            nw = int(sh*r); x0=(sw-nw)//2; img=img.crop((x0,0,x0+nw,sh))
        else:
            nh = int(sw/r); y0=(sh-nh)//2; img=img.crop((0,y0,sw,y0+nh))
        img = img.resize((TW,TH), Image.LANCZOS)
        img.save(out/f'{prefix}_slide{i+1:02d}.png','PNG')
    doc.close()

render(FORE_PDF, OUT_FORE, 'forensic')
render(FOG_PDF, OUT_FOG, 'fog')
"

# Film cut
ffmpeg -y -ss 0 -i 'PATH_TO_The_Hidden_Human_Repair_Load.mp4' \
  -t 45 -vf 'scale=1080:1920:flags=lanczos,setsar=1' \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 30 -an \
  social_engine_land/assets/film_cut/proof_brand_45s_vertical.mp4
```

To wire live keys and run a real brief (requires Infisical access):

```bash
# Set live env vars (values from Infisical — never commit them)
export XAI_API_KEY='...'        # or GROK_API_KEY
export TELEGRAM_BOT_TOKEN='...'
export TELEGRAM_WEBHOOK_SECRET='...'
export VENICE_API_KEY='...'
export POSTIZ_API_KEY='...'
export POSTIZ_API_URL='https://api.postiz.com'
export POSTIZ_INTEGRATION_LINKEDIN='...'
export POSTIZ_INTEGRATION_X='...'
export POSTIZ_INTEGRATION_INSTAGRAM='...'
export POSTIZ_INTEGRATION_FACEBOOK='...'
export POSTIZ_INTEGRATION_REDDIT='...'
export POSTIZ_INTEGRATION_YOUTUBE='...'
export SOCIAL_ENGINE_FAKE=0

# Start the server in live mode
cd social_engine_land/social_engine
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8088

# Submit a brief and approve it to push through to Postiz drafts
# (same curl pattern as fake mode, but with real keys the pipeline hits live services)
```

---

## GIT STATE (at session close)

- **Repo root:** `/Users/test`
- **Current branch:** `main` (no commits yet — this is a fresh repo)
- **Handoff branch:** `handoff/social-engine-2026-09-13` (pushed — see below)
- **Commit:** first commit on `handoff/social-engine-2026-09-13` containing:
  - `social_engine_land/PROOF_PLAN.md` (content plan)
  - `social_engine_land/SOCIAL_ENGINE.md` (project README)
  - `social_engine_land/upload_social_engine.py` (GitHub upload script)
  - `social_engine_land/social_engine/` — full engine source (app/, tests/, config, requirements, README)
  - `social_engine_land/social_engine/app/prompts.py` (PROOF-retooled)
  - `social_engine_land/social_engine/app/models.py` (PROOF CTA)
- **NOT committed (by choice):** `social_engine_land/assets/` (generated carousel PNGs and film MP4 — see DECISIONS), `.venv/`, `social_engine.sqlite*`, `.DS_Store` files.

---

*End of handoff.*

# Cold Brew v2: state
Status key: GENERATED = written, TESTED = run and checked, DEPLOYED = live, PLANNED.

| Item | Status | Notes |
|---|---|---|
| Brief, direction, DNA (dna.json) | GENERATED | Colors measured approximately with Pillow, not the skill's sharp script. |
| Poster (poster/poster.svg + poster.png, built by poster/build.py) | TESTED | Rendered in Chromium and viewed. Fonts embedded (OFL). |
| Video (video/index.html, audio.py, timing.js) | TESTED | Rendered 10 s, 1080x1920, 60 fps, AAC audio, in the sandbox with GSAP 3.15.0. Frames viewed. Audio measured (mean -22 dB, peak -0.9 dB), NOT listened to by the assistant. Not yet rendered on GitHub Actions. |
| Website (site/index.html) | TESTED (phone width 390px, local) | GSAP + ScrollTrigger from jsDelivr (intercepted locally in the sandbox, CDN itself not reached). DEPLOYED only after this branch is merged (GitHub Pages). |
| HyperFrames | PLANNED | Never run. |

Placeholders (marked * on every asset): brand name, 12 hr steep time, 350 ml, price. Language: English (default, not confirmed).
Render: Actions > "Render video" > project `cold-brew`, or locally `GSAP_DIR=<gsap/dist> python scripts/render_video.py cold-brew`.

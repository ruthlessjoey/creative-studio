---
name: video-ad-producer
description: Plans and builds short vertical video ads, including script, shot list, sound design, music, narration, and captions, rendered by scripts/render_video.py (Chromium + FFmpeg, tested on GitHub Actions). HyperFrames is a planned upgrade, not yet tested. Use for any video deliverable.
---

# Video Ad Producer

## Inputs
`briefs/<job>.md`, `projects/<job>/direction.md`

## Outputs (in `projects/<job>/video/`)
- `script.md`: one narration line, on-screen text, timings
- `shotlist.md`: shots with start/duration in seconds
- `index.html`: seekable composition exposing `window.renderFrame(t)` (9:16)
- `audio-plan.md`: music, SFX list, narration source, licenses

## Procedure
1. Write script and shot list for the brief's length (default 8s: hook 0-2s, product 2-6s, CTA 6-8s).
2. Audio plan:
   - Music: royalty-free or CC0 only. Record title, author, URL, license in `docs/credits.md`.
   - SFX: ice clink, pour, stir. Same license rule.
   - Narration: use a verified free TTS, otherwise the owner records a voice memo and uploads it.
   - Captions burned in for muted viewing.
3. Build `index.html` so every animation is a pure function of time `t` (no wall-clock, no unseeded randomness). Apply the motion-design skill for timing and easing.
4. Render with the "Render video" GitHub Actions workflow (runs `scripts/render_video.py <project>`). Verify by extracting frames and checking audio levels before reporting success.

## Quality criteria
Correct duration and 9:16 size; text readable on a phone; audio not clipped; every audio asset has a license entry; file under 20 MB.

## Failure handling
If render fails, save the error log to `projects/<job>/video/render-error.txt` and report it. Do not claim a video exists unless the MP4 was produced.

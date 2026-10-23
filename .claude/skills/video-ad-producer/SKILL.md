---
name: video-ad-producer
description: Plans and builds short vertical video ads, including script, shot list, sound design, music, narration, and captions, rendered with HyperFrames (HTML to MP4) in the HyperFrames GitHub Actions workflow. Legacy Playwright+FFmpeg renderer kept for older projects. Use for any video deliverable.
---

# Video Ad Producer

## Inputs
`briefs/<job>.md`, `projects/<job>/direction.md`

## Outputs (in `projects/<job>/video/`)
- `script.md`: one narration line, on-screen text, timings
- `shotlist.md`: shots with start/duration in seconds
- HyperFrames project: `projects/<job>/hyperframes/index.html` (root composition, `data-composition-id="main"`, GSAP timeline in `window.__timelines`), `assets/product/` (the supplied photos, unmodified), `assets/fonts/`, `assets/audio/`
- Legacy projects (coffee-launch, cold-brew) use `video/index.html` + `window.renderFrame(t)` + `scripts/render_video.py`
- `audio-plan.md`: music, SFX list, narration source, licenses

## Procedure
1. Write script and shot list for the brief's length (default 8s: hook 0-2s, product 2-6s, CTA 6-8s).
2. Audio plan:
   - Music: royalty-free or CC0 only. Record title, author, URL, license in `docs/credits.md`.
   - SFX: ice clink, pour, stir. Same license rule.
   - Narration: use a verified free TTS, otherwise the owner records a voice memo and uploads it.
   - Captions burned in for muted viewing.
3. Build the HyperFrames composition following `.claude/skills/hyperframes/SKILL.md` (the contract: `.clip` + `data-start`/`data-duration`, one paused GSAP timeline registered in `window.__timelines`, no wall-clock, no random, no CSS filters for grades, only bundled or `@font-face` fonts). Apply the motion-design skill for timing and easing, creative-director for the concept.
4. Product shots come from the supplied photographs (crops, pushes, pans). Never replace the product with drawn code.
5. Gate and render with `.github/workflows/hyperframes-render.yml`: `npx hyperframes@<pin> check --json`, `snapshot`, `render --quality delivery`, then ffprobe checks (duration, 1080x1920, audio stream). Look at the snapshot PNGs before reporting.
6. Sandbox note: if npm is unreachable (as in the Claude cloud sandbox), do not substitute another rasterizer for the final video. Run the workflow on GitHub instead and report the status honestly.

## Quality criteria
Correct duration and 9:16 size; text readable on a phone; audio not clipped; every audio asset has a license entry; file under 20 MB.

## Failure handling
If render fails, save the error log next to the project and report it. Do not claim a video exists unless the MP4 was produced and validated. Synthesized audio is a placeholder and must be labeled as such.

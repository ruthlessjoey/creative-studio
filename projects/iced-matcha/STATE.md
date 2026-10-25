# Iced Matcha: state (GENERATED / TESTED / DEPLOYED / PLANNED / BLOCKED)

| Item | Status | Notes |
|---|---|---|
| Real product photo as primary asset | GENERATED | Copied unmodified into hyperframes/assets/product/. All 9 scenes read it via the `product` variable. No code-drawn cup anywhere. |
| HyperFrames composition (index.html, 10 s, 1080x1920) | GENERATED | Follows the HyperFrames contract. Previewed here with a plain-Chromium seek harness (NOT HyperFrames): key frames viewed. |
| `hyperframes check` / `snapshot` / `render` | TESTED (GitHub Actions) | hyperframes@0.8.185 on ubuntu-latest: `check` ok (0 errors; 11 lint, 1 layout, 4 craft warnings: scenes not yet split into sub-compositions, short 1 s text holds from the storyboard timing). Render 10.0 s, 1080x1920, h264 + aac, validated with ffprobe. Frames extracted from the MP4 and viewed. Cannot run in the Claude sandbox (npm unreachable); the workflow is the runtime. |
| MP4 | TESTED | `out/iced-matcha-9x16-share.mp4` (about 12 MB, crf 27 copy). The full-quality delivery render (about 115 MB) is only in the workflow artifact. |
| Foley audio (assets/audio/foley.wav) | TESTED (measured only) | Synthesized placeholder (room tone, whooshes, ice ticks, pour). Present in the MP4: mean -27 dB, peak -1.5 dB. Not listened to by the assistant. Replace with real recordings. |
| Poster 4:5 (poster/poster-4x5.png) | TESTED | Static HTML/CSS over the unmodified photo, rendered with Chromium and viewed. No video render needed. |

## Blockers / limits (honest)
- Only ONE photo was supplied (1170x1170). 9:16 crops are upscaled up to ~3.4x, so close-ups are soft. A higher-resolution original fixes this.
- Storyboard scene 03 (pour) and 06 (top view) need shots that the photo does not contain. The film uses labeled crops (marbling, ice surface) instead. Next step: supply pour and top-down photos/clips, or approve an image-editing workflow (output would be labeled AI-modified).
- Scene 05 (lifestyle with plants) uses the photo's own sun/shadow wall; plants would need a new asset.
- Glass has no logo or label, so none is added.
- HyperFrames version pinned: hyperframes@0.8.185. GSAP in the composition comes from jsDelivr (3.14.2, as in the official blank template); the render needs internet on the runner.

## Follow-ups
- Split the 9 scenes into `compositions/*.html` sub-compositions (HyperFrames lint recommends it; needs a render to re-verify).
- Real foley, a higher-resolution photo, pour and top-down shots.
- Square and landscape versions: set `data-width/height` and recompose; not requested yet.
- The earlier procedural 3D glass lives only on branch `matcha-3d` and is not used (product must come from photos).

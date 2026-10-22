# Iced Matcha: state (GENERATED / TESTED / DEPLOYED / PLANNED / BLOCKED)

| Item | Status | Notes |
|---|---|---|
| Real product photo as primary asset | GENERATED | Copied unmodified into hyperframes/assets/product/. All 9 scenes read it via the `product` variable. No code-drawn cup anywhere. |
| HyperFrames composition (index.html, 10 s, 1080x1920) | GENERATED | Follows the HyperFrames contract. Previewed here with a plain-Chromium seek harness (NOT HyperFrames): key frames viewed. |
| `hyperframes check` / `snapshot` / `render` | PLANNED | Cannot run in the Claude sandbox (npm registry unreachable). Runs in `.github/workflows/hyperframes-render.yml` on GitHub. Not claimed until that run is green. |
| Foley audio (assets/audio/foley.wav) | GENERATED | Synthesized placeholder (room tone, whooshes, ice ticks, pour). Not listened to. Replace with real recordings. |
| Poster 4:5 | see poster/ | built from the same photo |

## Blockers / limits (honest)
- Only ONE photo was supplied (1170x1170). 9:16 crops are upscaled up to ~3.4x, so close-ups are soft. A higher-resolution original fixes this.
- Storyboard scene 03 (pour) and 06 (top view) need shots that the photo does not contain. The film uses labeled crops (marbling, ice surface) instead. Next step: supply pour and top-down photos/clips, or approve an image-editing workflow (output would be labeled AI-modified).
- Scene 05 (lifestyle with plants) uses the photo's own sun/shadow wall; plants would need a new asset.
- Glass has no logo or label, so none is added.
- HyperFrames version pinned: hyperframes@0.8.185. GSAP in the composition comes from jsDelivr (3.14.2, as in the official blank template); the render needs internet on the runner.

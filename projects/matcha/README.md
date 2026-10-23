# matcha (PARKED EXPERIMENT, not a deliverable)

**Status: unfinished and untested. Nothing in this branch is production-ready.**

This is a procedural three.js experiment: a code-drawn iced matcha glass (glass, liquid, ice, straw, droplets) in front of giant stacked "MATCHA" type. It was parked because the project rule is that the product must come from the real photograph, never from a code-drawn drink. The photo-first work lives on branch `iced-matcha-hyperframes` (`projects/iced-matcha/`). That branch was not touched by this README.

## Branch facts
- Branch: `matcha-3d`
- Known starting commit: `ac11d69` ("experiment: procedural 3D matcha (three.js)...")
- HEAD inspected before adding this README: `ac11d6995d0e4e75a8ce097e8bdc09916936cd02` (local and remote were identical)
- The commit that adds this README is the only change after that.

## What was and was not verified

| Item | Status |
|---|---|
| Full 600-frame video render (10 s at 60 fps, 1080x1920) | **Killed before finishing.** No complete render exists. |
| Per-frame cost | Reportedly about 4.4 s per frame at 1080x1920 in a test (software WebGL, 2 CPU cores). Recorded from an earlier session; not re-measured here. |
| Final video (`video/out/matcha-9x16.mp4`) | **Does not exist** on this branch. |
| Poster (`poster/poster.png`) | **Does not exist.** `poster/index.html` was never rendered or verified. |
| Site (`site/index.html`) | **Never tested** in a browser. It references `../poster/poster.png` and `../video/out/matcha-9x16.mp4`, neither of which exists, so its fallback image and video are broken links. |
| Audio (`video/audio.py`) | Synthesized placeholder; not verified. |

## Files
- `scene/scene.js`: `createScene()` builds the whole 3D scene (three.js r186). Procedural glass (`LatheGeometry` + `MeshPhysicalMaterial` transmission), shader liquid (`LIQ_FS`), ice (`roundedCube`), straw, pour stream, 150 instanced droplets, dust particles, a PMREM studio environment, contact-shadow and glow decals, and a 2D-canvas "MATCHA" backdrop texture on a flat plane.
- `scene/test.html`: tiny harness for `createScene`.
- `video/index.html`, `video/timing.js`, `video/audio.py`: 10 s 9:16 composition driven by `renderFrame(t)`, with a GSAP overlay timeline.
- `poster/index.html`, `site/index.html`: poster and scroll/drag site built on the same scene.
- `../../scripts/render_video.py`: this branch adds parallel WebGL frame workers and `RESUME` support to the legacy Playwright + FFmpeg renderer.
- `../../assets/vendor/three/`: three.js r186 core files and `RoomEnvironment.js` (MIT).
- `../../.claude/skills/threejs-*`: ten three.js skill files (documentation only).

## Known limitations
- The drink is code-generated. It must not be used as the product.
- Dimensional typography is **not** implemented. The "MATCHA" type is 2D `fillText` onto a canvas texture on a flat plane. No `TextGeometry`, `FontLoader` or extrusion exists, and those addons are not vendored.
- No post-processing: no `EffectComposer`, bloom or depth of field, and none of those addons are vendored.
- No transparent output: the renderer is opaque, so the scene cannot yet be composited over the photo.
- Very slow on a CPU-only runner (see above). Never profiled.
- The GSAP script tag points at a CDN; the renderer only swaps in a local copy if `GSAP_DIR` or `node_modules/gsap/dist` exists.
- The Playwright/SwiftShader flags in `render_video.py` were used on a sandbox machine; behavior on a GitHub Actions runner was not tested for this branch.
- No `STATE.md` existed before this README.

## Rule
Do not merge, deploy or ship anything from this branch. It is kept only as a code reference for techniques (camera paths, deterministic time-driven scenes, parallel frame rendering). See the audit notes in the project conversation / next-phase plan before reusing any of it.

---
name: studio-router
description: Entry point for any creative job. Reads the brief, picks only the skills needed, and keeps context small. Use first for any design, video, ad, or website request.
---

# Studio Router

## Procedure
1. Read `briefs/<job>.md`. If none exists, ask max 3 questions, then write one.
2. List deliverables. Activate only the matching skills:
   - concept, mood, plan -> creative-director
   - palette, type, layout, landing page, UI review -> ui-ux-pro-max (run its search script; treat output as advice, cross-check against the brief)
   - analyze a reference image/site into tokens and style -> design-dna
   - timing, easing, choreography, animation feel -> motion-design
   - video, motion graphics, ad, reel, short -> video-ad-producer, which builds and renders with HyperFrames (read `.claude/skills/hyperframes/SKILL.md` first, then hyperframes-cli)
   - poster, still, social post, square or landscape image -> a static layout (HTML/CSS or SVG screenshot). Do NOT start a video render for a still.
3. PRODUCT PHOTO RULE: if the user supplied product photos, those photos are the product. Copy them unmodified to `projects/<job>/.../assets/product/` and pass them into scenes by path. Never redraw the product as CSS, SVG or code, and never silently generate a replacement. If a shot needs something the photos do not show (pour, top view, another environment), say so and list it as a missing asset in STATE.md; use only labeled crops, or an image-edit workflow whose output is marked AI-modified.
4. Prefer deterministic tools (SVG, CSS, FFmpeg, scripts) over AI generation.
5. After each stage, write a 5-line summary to `projects/<job>/STATE.md`. Later stages read STATE.md, not the full history.
6. Never reread unchanged assets. Never add a paid API.

## Honesty rule
In STATE.md mark every item as: PLANNED, GENERATED, TESTED, or DEPLOYED. Never mark TESTED without actually running it.

## Failure handling
If a tool needs a computer or paid service, say so and give the free alternative or the manual step.

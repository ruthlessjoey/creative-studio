---
name: studio-router
description: Entry point for any creative job. Reads the brief, picks only the skills needed, and keeps context small. Use first for any design, video, ad, or website request.
---

# Studio Router

## Procedure
1. Read `briefs/<job>.md`. If none exists, ask max 3 questions, then write one.
2. List deliverables. Activate only the matching skills:
   - concept, mood, plan -> creative-director
   - video, motion, audio -> video-ad-producer
3. Prefer deterministic tools (SVG, CSS, FFmpeg, scripts) over AI generation.
4. After each stage, write a 5-line summary to `projects/<job>/STATE.md`. Later stages read STATE.md, not the full history.
5. Never reread unchanged assets. Never add a paid API.

## Honesty rule
In STATE.md mark every item as: PLANNED, GENERATED, TESTED, or DEPLOYED. Never mark TESTED without actually running it.

## Failure handling
If a tool needs a computer or paid service, say so and give the free alternative or the manual step.

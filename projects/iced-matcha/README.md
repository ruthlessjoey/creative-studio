# Iced Matcha: how to run

Simplest free way (nothing to install): GitHub > Actions > "HyperFrames render" > Run workflow (project `iced-matcha`). It runs `npx hyperframes@0.8.185 check`, `snapshot`, `render`, validates the MP4 with ffprobe, uploads it as an artifact, and commits it to the branch under `projects/iced-matcha/out/`.
It also runs automatically on every push that touches `projects/iced-matcha/hyperframes/**` on the `iced-matcha-hyperframes` branch.

On a computer (Node 22+, FFmpeg):
```
cd projects/iced-matcha/hyperframes
npx hyperframes@0.8.185 preview     # edit in the browser
npx hyperframes@0.8.185 check
npx hyperframes@0.8.185 render --quality delivery --output ../out/iced-matcha-9x16.mp4
```
Swap the product photo: replace `assets/product/iced-matcha.jpg` (or set the `product` variable). Crops are defined in `index.html` (`crop(L,T,W)` = left, top, width in photo pixels).
iPhone: you can edit text/timings in `index.html` on GitHub, then push: the workflow re-renders.

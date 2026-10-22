# Third-party skills and tools

Every external skill was read before install: file inventory, license, scripts, network and exec calls,
credential access, prompt-injection phrasing, hidden Unicode, symlinks, install hooks, and requested tool permissions.
Skills are vendored as **pinned snapshots** (no live auto-update), each with its upstream LICENSE beside it.
Re-vet before updating any of them. Vetting date: 2026-10-22.

## Installed (in `.claude/skills/`)

| Skill | Source | License | Pinned commit | Copied | Left out |
|---|---|---|---|---|---|
| ui-ux-pro-max v2.15.0 | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | MIT | 623a9a9037d006ea727f8213f084d02a6b6f11b5 | `.claude/skills/ui-ux-pro-max/` (data, scripts, references) | tests, CLI, gallery, other bundled skills, premium features |
| design-dna | https://github.com/zanwei/design-dna | MIT | 593e39bc9e3652734653bd75544a333d7d43615e | SKILL.md, references/ | optional Node scripts (need native `sharp` package), translated READMEs, images |
| motion-design | https://github.com/lottiefiles/motion-design-skill | MIT | f9a8a041b85185ee4881b3471d3415e939aac772 | whole `skills/motion-design/` (Markdown only) | none |

Checks on the installed tree: 0 symlinks, 0 network or exec calls in the skills, 0 injection phrases, 0 hidden characters,
no `allowed-tools` or `hooks` declared. ui-ux-pro-max Python uses the standard library only and ran offline (0.19 s).

## Approved but NOT installed

| Item | Source | License | Reviewed commit | Why not yet |
|---|---|---|---|---|
| threejs-skills | https://github.com/CloudAI-X/threejs-skills | MIT | 0e181866f095b5f06d005133876e926515390d95 | 13 Markdown skills, no scripts, safe. Install only when a 3D task needs it (keeps skill list small). |
| genjutsu v4.1.1 | https://github.com/AThevon/genjutsu | MIT | 1f518a71378b15d423389e546e767cffc86e14c3 | Safe (no hooks, scripts are dev tooling) but heavy: three skills of 46 to 67 KB each, a multi-subagent orchestrator, and a vendored copy of ui-ux-pro-max (duplicate). Evaluate one skill at a time. |
| HyperFrames | https://github.com/heygen-com/hyperframes | Apache-2.0 | 4371981b740d92f70e520cfbec34db68a1c93434 | Never run yet. To be trialled in GitHub Actions. Its docs show example calls to paid transcription APIs (OpenAI, Groq): do not use. |
| GSAP 3.15.0 | https://github.com/greensock/GSAP | GreenSock "Standard No Charge" license (free incl. commercial; NOT open source) | 13e2b790546426a1a2e0e9b409f3f8dc6d6611f2 | Not vendored. Load from npm/CDN. Prohibited: using it in a visual no-code animation builder that competes with Webflow. Do not remove its notices. |

## Rules
- No paid API is a dependency. Examples in upstream docs that need keys are ignored.
- Never commit secrets. Workflows use only the built-in `GITHUB_TOKEN`.

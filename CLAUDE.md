# CLAUDE.md — Fleet

Guidance for Claude Code sessions operating in this repository.

## What Fleet is

Fleet is the **public-facing companion** to private research on edge-sensor compression conducted by Peripheral Technologies LLC. It is read by researchers, engineers, collaborators, and anyone curious about how language models might one day talk to physical sensors at the codec layer.

This repo is a **curated shelf**, not a working notebook. Everything that lands here is deliberate.

## Hard rules — never violate

1. **Never import, reference, or paraphrase content from private repos.** This includes `periphera`, `peripheral`, `peripheral-protocol`, or any other private work. Treat them as if they don't exist when operating here.

2. **No production codecs.** BTQ-SafeGray, BTQ-Safe, Quip, DCT-BlockTQ, E8 Shell, Tangent-Space Shell, Monodromy, ChromaDual, GyroEcho, and any unnamed-but-novel variant in private work stay private. Fleet may host **public prior-art codecs** (TurboQuant, USQ, scalar quantization) or **deliberately simplified demonstrations**.

3. **No benchmark numbers from private research.** Do not publish SF, CRF, BER, Kendall tau, or comparative performance data from private experiments. If Fleet needs benchmark numbers, they must come from runs performed in this repo on public datasets with publicly-described methodology.

4. **No firmware, no C ports, no embedded-specific IP.** The libgist C port and its patterns stay private. Fleet may include portable reference implementations in Python or standard C, but nothing that reveals the embedded tuning.

5. **No evidence trails or internal verdicts.** The `evidence/`, `experiments/`, `spec/`, and `conformance/` patterns from private repos stay private. Fleet's testing/eval posture is its own — light, clear, and public-appropriate.

6. **If in doubt, don't publish.** When unsure whether something belongs here, the default is no. Ask the user before publishing any content that references private work, even obliquely.

## What belongs here

- Reference codec implementations that are **public prior art** or **deliberately simplified demonstrations**
- Protocol sketches — wire formats, MCP bridges, closed-loop patterns — that show *architecture* without revealing production tuning
- Harnesses and evaluation scaffolds where the harness itself is the contribution
- Short writeups (notes, walkthroughs, explainers) on ideas safe to share
- Small, well-scoped tools that help the community

## Style and tone

Write for the reader, not for the author.

- **Plain language** — short sentences, common words, no internal jargon
- **Lead with what the reader wants** — what does this do, when would I use it, how do I run it
- **Name things for clarity** — a reader should understand a folder name without opening it
- **Tone**: inviting, not marketing; confident, not boastful; technical, not academic
- **No emojis** unless the user explicitly asks
- **No hype** — no "revolutionary," "first-of-its-kind," "unprecedented." Let the work speak.
- **Attribution matters** — when a technique has prior art (TurboQuant, E8 lattice, etc.), credit it

## Commits and PRs

- Atomic commits, present tense, specific subjects ("add TurboQuant reference impl" not "update code")
- PRs welcome from the community; PR descriptions state the "why" and link to any related issues
- Never force-push to main
- Every commit must be safe to publish — no auto-revertible slip-ups

## When Claude Code is adding content to Fleet

Before writing or committing, check:

1. **Source check** — where does this content come from? If the answer involves any private repo, stop and ask the user.
2. **Posture check** — does this reveal architecture (OK) or performance/tuning/moat (not OK)?
3. **Audience check** — will a reader coming in fresh understand what this is and why it exists?
4. **Scope check** — does this fit the "curated shelf" purpose, or is it notebook material that should stay private?

If any check is unclear, ask before proceeding.

## When Claude Code is responding to community contributions

- Be gracious and specific — thank, then give concrete feedback
- If a contribution touches anything near private work, escalate to the user before merging
- Quality bar matches the repo's posture — careful, clear, public-appropriate

## Branching

Fleet uses standard `main` with topic branches. Branch names follow `<type>/<topic>` — e.g., `feat/mcp-bridge-example`, `docs/turboquant-walkthrough`. No worktree discipline needed here.

## License

Apache-2.0. All contributions are accepted under the same license, including its patent-grant clause. This is intentional — Fleet is meant to be built on.

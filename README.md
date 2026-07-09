# goal-opus — a self-improving goal loop for Claude Code

This repo is an **agent home**: a set of Claude Code skills, subagents, and durable
memory that together implement a generator/evaluator loop with independent adversarial
verification and mandatory write-back. Every run makes the system slightly better at
running, because confirmed lessons are distilled into rules and written back into the
skills and memory that the next run inherits.

## The core contract

1. **Define done first.** Before any building, "done" is written as an executable,
   Default-FAIL rubric (`criteria.json`) — every criterion starts `failing` and has an
   exact verify command or read-only procedure. The human signs off on the WHAT, never
   the HOW.
2. **Maker ≠ grader.** A `goal-maker` agent builds; a fresh-context `goal-verifier`
   agent grades against the locked rubric without ever seeing the maker's reasoning.
   The verifier never edits files; only the orchestrator writes `criteria.json`.
3. **Write before walking.** A run is not finished until its write-back phase has run —
   on success, abort, or cancel alike. The confirmed lesson lands in `STATE.md` or the
   skill itself, as a reviewable git diff.

## What's in the box

| Piece | What it does |
|---|---|
| `/goal-opus <goal>` | The loop: rehydrate → rubric → make → verify → gate → distill → commit. Maker and verifier both run on Opus. |
| `/prd <product statement>` | Research-first PRD generator (documents only, never code): 3-agent research fan-out, untold-requirements mining, adversarial gap check, then a PRD + seeded rubric that `/goal-opus` executes. |
| `/deep-prd` | Same as `/prd` but forces the deep-research workflow (requires the deep-research plugin; fails loudly without it). |
| `/design-direction` | Interactive session that freezes a design direction + banned-visuals list, so UI goals can be graded by *looking* (vision-verify) instead of by text. |
| `.claude/agents/` | `goal-maker` and `goal-verifier` definitions. |
| `STATE.md` | The durable memory: verified facts, general rules, decision log, lessons. Read at every session start via its Rehydration protocol. |
| `docs/context/` | The design substrate (files 01–11) the system was built from. |
| `goals/` | Evidence from past runs — rubrics, verifier verdicts, progress logs. Doubles as the eval suite for regression-checking the system after self-edits. |
| `tools/rubric_check.py` | Lint for rubrics at Phase 1 sign-off. |

## Getting started

1. **Prerequisites:** [Claude Code](https://claude.com/claude-code) with access to
   Claude Opus 4.8 (the skills pin `model: claude-opus-4-8` for maker and verifier).
   `/deep-prd` additionally needs the deep-research plugin.
2. Clone this repo and start Claude Code at its root. `CLAUDE.md` (invariants) and
   `STATE.md` (memory) are picked up automatically; skills register from
   `.claude/skills/` — agent definitions need a fresh session to become spawnable, so
   don't test from the session that scaffolded them.
3. First run: `/prd "<what you want to build>"` → review the PRD and seeded rubric →
   `/goal-opus "<first phase from the PRD>"`.

**Home vs. target:** this repo is never a build target. Every product-code goal
declares a TARGET repo where the product code (and that project's own `STATE.md`)
lives; only the system, its memory, and run evidence live here. Don't clone this repo
per project — that forks the self-improving skill and splinters the compounding.

## Invariants (short version)

The authoritative list lives in [CLAUDE.md](CLAUDE.md). In brief: independent
verification of every output; maker never grades; PRDs never contain code; visual work
is verified by looking at screenshots, not by reading about them; retrieval is
grep/Glob/Read over live files (no embedding index, no persistent code graph);
improvement means editing files — never assuming the model changed.

## A note on this repo's history

The public repo starts from a fresh initial release. `STATE.md` occasionally cites
pre-release commit hashes as evidence pointers; those resolve only in the author's
private archive, not here. Everything needed to run the system is in the tree.

## License

[MIT](LICENSE)

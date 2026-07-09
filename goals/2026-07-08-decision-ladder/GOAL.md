# Goal — distill the lazy-senior-dev decision ladder into the loop (D8 ADOPT, Goal 1)

Add a minimalism-with-completeness discipline to the goal loop **without any plugin
dependency** — plain text edits to existing skill/agent files only. No hooks, no MCP.

## The canonical ladder (must appear verbatim, in this priority order)
Before writing any new code, walk this ladder top-down and stop at the first rung that
solves it; justify any rung you skip:
1. Does it need to exist at all? (YAGNI)
2. Already in the codebase?
3. In the standard library?
4. Native platform feature?
5. Installed dependency?
6. One-liner solution?
7. Only then: minimum viable implementation.

## The three edits
1. `goal-maker.md` RULES gain the ladder (verbatim, ordered, with justify-skips).
2. The goal-opus maker packet + maker return contract gain a **completeness
   counter-guard**: before declaring work ready, the maker must enumerate every
   criteria.json id with an explicit satisfied / not-satisfied line (YAGNI must never
   silently drop rubric-mandated work — the canonical failure is a one-liner that
   removed input validation and shipped a directory-traversal bug).
3. `goal-verifier.md` gains an **over-engineering / under-implementation lens** that
   can fail an artifact in EITHER direction: (a) unrequested complexity, (b) dropped
   rubric-mandated edge/empty/error/validation states — with the dropped-input-
   validation case named as the canonical example.

Plus fixtures for C4: three small Python samples under this goal's `fixtures/`
(`overbuilt.py` — solves a trivial task with unrequested abstraction layers;
`missing_validation.py` — a "minimal" file-serving snippet whose validation was
YAGNI'd away; `minimal_ok.py` — correct minimal solution) so the verifier can prove
the lens classifies all three correctly.

TARGET: agent home (D:\horil\agent) — system work, allowed per scope rules.

## Provenance
- From `docs/research/2026-07-08-tooling-augmentation.md` §Top-3 Goal 1 (verdict D8).
- Rubric sign-off: user approved running this goal ("go run both 1 and 3 in order").

# Progress log — 2026-07-08-retrieval-invariant

Maker handoff memory. One entry per iteration, appended by goal-maker.
The verifier never reads this file.

---

## Iteration 1 — 2026-07-08

**Changed:**
- New substrate file `docs/context/11-retrieval-invariant.md` (follows pack numbering,
  pack voice + tags). Records the measured asymmetry (grep 0.92 vs graph 0.83 overall;
  graphs win only structural queries) with `arxiv.org/html/2603.27277v1` tagged
  **[VERIFIED+SRC 3-0]**; the Anthropic-abandoned-RAG rationale tagged **[REPORTED]**;
  the self-rewriting-maker staleness argument; and the single verifier-only, one-shot,
  frozen-artifact exception gated on demonstrated verifier token-bleed on structural
  criteria on a specific goal. (C2, C3)
- `CLAUDE.md` gains one Invariants bullet (5 added lines, 0 removed — under the 6 cap)
  naming both rejected classes with a one-line reason each and linking to file 11. (C1)
- `.claude/skills/prd/SKILL.md` Phase 2 gains a "Loop-retrieval guard" paragraph
  cross-linking the invariant so PRD research does not re-propose RAG/graphs for the
  loop itself. Inserted well above the append-only sections (untouched). (C4)

**Why:** D8 ADOPT / Goal 3 — freeze the primitives-first retrieval decision so future
runs never re-litigate it. Evidence source: `docs/research/2026-07-08-tooling-augmentation.md`
(Candidates 2 & 4).

**Line-count note for next iteration:** the 6-line CLAUDE.md cap is hard. I did NOT
update the stale "files 01–10" range on CLAUDE.md line 5 (README also still says 01–10
and is out of allowed scope) — kept CLAUDE.md additions at 5 for margin. Tags copied
verbatim from the report; never upgrade [REPORTED] → [VERIFIED].
git status is scoped to CLAUDE.md + file 11 + prd SKILL.md + this workdir (C4).

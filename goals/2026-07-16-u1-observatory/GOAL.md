# GOAL — U1: read-only observatory (agentic-os Mission Control, first UI slice)

## Goal statement (verbatim)
U1 — read-only observatory (loopback + Host-validation reader, the 4 mechanics as 4
panels, live update with a staleness indicator, torn-read-safe reader, empty/first-run/
not-installed/crash states, a11y baseline), target: D:\horil\agentic-os

## TARGET
`D:\horil\agentic-os` — the agentic-os framework repo (the engine this UI observes).
Product code lands there under a new `ui/` tree + a `dash` verb on `cli/agentic_os.py`.
Run evidence (this dir) stays in the agent home.

## Context this run inherits
- This is **U1** of the phased UI roadmap in `docs/UI-PRD.md` §7 — "the floor."
- The design direction is **FROZEN** (U0 done 2026-07-16): `docs/design/design-direction.md`
  v1 — direction **C · "Helm"** (continuous near-black canvas + slim nav rail + right truth
  rail; centered living-loop graph). Anchors present: `references/R3-helm-home-live-run.png`
  (primary), `mocks/helm-home-live-run.reference.html`, `mocks/contrast-check.py`. B13
  satisfied.
- Whole-product PRD + seed: `docs/UI-PRD.md`, `docs/ui-criteria.seed.json` (C1–C14). This
  run scopes the **U1 subset**; U2 (living-loop motion + flight-recorder + virtualized
  run-log), U3 (dedicated skills-inventory surface + onboarding + glossary), U4 (control),
  and C14 (live ≥2-goal acceptance) are OUT OF SCOPE here.
- Engine data model is **code-verified** (`cli/agentic_os.py`): `.agentic-os/run-status.json`
  (written in place, non-atomic → torn reads real), `.agentic-os/run-log.jsonl` (append-only
  events incl. `session_start`/`iteration`/`land_gate`/`session_end`), `.agentic-os/queue.json`,
  `STATE.md`. Fields: `in_flight={goal,iter}` (crash marker), `totals.{criteria_passing,
  criteria_total,cumulative_tokens}`, `budgets.{iteration_budget,token_budget}`, per-goal
  `goals[].{id,state,criteria_passing,criteria_total,...}`. The CLI scrub covers run-log +
  notify but **NOT** STATE.md / run-status.json (code-verified) → the UI must re-redact.

## Scope decisions (orchestrator, Phase 1)
- **Living loop is IN U1 as a STATIC panel** — the design direction identifies the active
  stage statically (color + icon + "YOU ARE HERE" label + position; NO idle pulse), and R3
  (the vision-verify anchor) has it centered. The MOTION (one-shot marker transition),
  flight-recorder timeline, and virtualized run-log are **U2**.
- **Skills panel is IN U1 at the home-rail richness R3 shows** (name/version/scope/
  permissions/enabled-vs-active/standing-cost + update triad) — BV5/B11 ban the bare list.
  The dedicated `skills-inventory` surface + broken/degraded state + "did it fire" from
  run-log analysis are **U3**.
- **Transport = polling** (1–2s) is an accepted v1 fallback (PRD U7). SSE not required in U1.
- **No live `claude` needed:** every U1 criterion is gradeable against **fixtures**
  (torn/crash/non-monotonic/stale/secret) + **re-captured screenshots** (vision-verify).
  Deterministic — the MOCK-VERIFIED≠LIVE-READY hazard is low here (U1 reads static files;
  no non-deterministic dependency). C14's live run is deferred to the whole-product gate.

## Sign-off
**APPROVED AS DRAFTED** by the user at Phase 1 (2026-07-16) — 12 criteria (C1–C9, C11,
C12, C13, C15), 20 banned outcomes (BV1–BV16 verbatim + B3/B4/B12 + scope guard), and the
three scope calls (static living-loop in U1, R3-rich skills, polling + in-memory
drop-history). rubric_check PASS. Proceeding to Phase 2.

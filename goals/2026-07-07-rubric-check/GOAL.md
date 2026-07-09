# Goal — rubric-check validator

Create `tools/rubric_check.py`: a CLI validator for goal-opus `criteria.json` files.
Invocation: `python tools/rubric_check.py <path-to-criteria.json>` → exit 0 if valid,
exit 1 with a message naming every problem if not.

Validation rules:
- Top-level keys: `goal`, `created`, `max_iterations` (int ≥ 1), `status` (one of
  `in_progress` | `success` | `aborted`), `criteria` (non-empty list),
  `banned_outcomes` (non-empty list).
- Every criterion: unique `id`, non-empty `statement`, non-empty `verify`, `status` in
  {`failing`, `passing`}; a `passing` criterion must have non-null `evidence`.
- Every banned outcome: unique `id`, non-empty `statement`, non-empty `verify`.

TARGET: agent home (D:\horil\agent) — system tooling, allowed per scope rules.

## Provenance
- E2E verification of REGISTERED agent routing (goal-maker / goal-verifier resolved
  from .claude/agents/ with their frontmatter models and tool allowlists) — closes the
  open item in STATE.md `Last session`.
- Also produces a real Phase-1 aid: rubric validation before sign-off.
- Rubric sign-off: unattended continuation of the approved verification plan.

# Progress log — 2026-07-07-rubric-check

Maker handoff memory. One entry per iteration, appended by goal-maker.
The verifier never reads this file.

---

## Iteration 1 (2026-07-07)

What I built:
- `tools/rubric_check.py` — CLI validator. `python tools/rubric_check.py <path>`.
  Exits 0 if valid, 1 if invalid (prints EVERY problem found to stderr, one per
  line, prefixed `INVALID: <path> (N problem(s))`), 2 on usage error (no path).
  Core is `validate(dict) -> list[str]` (collects all problems, never fail-fast)
  plus `check_file(path)` that wraps read + JSON-parse errors into the same list.
- `tools/tests/fixtures/bad_rubric.json` — malformed fixture for C3: criterion
  C1 is missing `verify`, and `banned_outcomes` is `[]`. Validator reports both.
- `tools/tests/test_rubric_check.py` — 19 tests (CLI subprocess tests for the two
  real rubrics + the bad fixture, plus unit tests of `validate`/`check_file`).

Design notes / gotchas for next iteration:
- max_iterations: JSON `true`/`false` parse to Python bool, which is an int
  subclass. `_is_int` rejects bools explicitly so `max_iterations: true` fails.
- A PASSING criterion needs non-null `evidence`; a FAILING criterion may have
  null evidence. The abort-probe rubric (C2) is a failing criterion with
  non-null evidence + top-level status `aborted` — accepted. This distinction is
  the subtle part; keep it if you refactor.
- Verify commands run from repo root D:\horil\agent (PowerShell). Confirmed all
  four verify commands and both banned outcomes (B1 no net imports, B2 clean
  git diff on criteria.json) pass there.

Results:
- C1 exit 0 (wordfreq accepted). C2 exit 0 (abort-probe accepted).
- C3 exit 1, output contains both "verify" and "banned_outcomes".
- C4: `python -m pytest tools/tests/test_rubric_check.py -q` -> 19 passed.
- Full suite `tools/tests/` -> 27 passed (8 wordfreq untouched + 19 new).

---

# Goal — wordfreq CLI

Create `tools/wordfreq.py`, a CLI that prints the top-N most frequent words of a text
file, with pytest tests under `tools/tests/`.

- Invocation: `python tools/wordfreq.py <file> <N>`
- Output: one `word count` pair per line, most frequent first.
- Words are case-insensitive; ties broken alphabetically.
- Edge cases: empty file → no output, exit 0.

## Provenance
- E2E verification run 1 for the /goal-opus system (see plan + STATE.md Last session).
- Rubric sign-off: run unattended by user pre-approval of the implementation plan
  (the plan, including this exact goal and rubric shape, was approved in plan mode).

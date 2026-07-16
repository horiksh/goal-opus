# Progress log — 2026-07-12-p4-observability-notification

Maker handoff memory. One entry per iteration, appended by goal-maker.
The verifier never reads this file.

---

## Iteration 1 — 2026-07-12
- **Changed (all in TARGET `D:\horil\agentic-os`; committed there, NOT in the home):**
  - `cli/agentic_os.py` (+218/-6): P4 observability + notification, extending the
    P1–P3 loop. No new run backend.
    - **OP1 tailable run-status:** added top-level `active_goal` + `active_iteration`
      to `run-status.json`, (re)written PER ITERATION at goal-start, iter-begin,
      iter-complete, and every terminal transition (reuses the existing `flush()`
      per-iteration write). Restored on resume.
    - **OP2 at-a-glance:** `status` now prints a compact one-view `AT A GLANCE` line
      (`state · goal · iter=N/max · criteria=p/t · tokens=cum/budget · mode`) above
      the existing detail. New `status --follow`/`--watch` (`--interval`,
      `--follow-timeout`) tails the file; bounded so it never hangs. Plain text only.
    - **OP3 push-notify (U35):** new `_notify()` fires on the FOUR notable events —
      `finish`(success), `block`(AGENT_STOP halt / land-gate flag / held),
      `budget`(budget-abort), `decline`. Wired via a `_NOTIFY_EVENT_FOR_STATE` map in
      `finalize()` (fires once per goal terminal, never per ordinary iteration) plus
      explicit session-level notifies in the AGENT_STOP halt path and
      `_finish_budget_abort` (those two pass `notify=False` into `finalize` to avoid
      double-firing). `finalize()` now returns the effective state.
    - **OP4 optional/non-fatal/local/scrubbed:** hook is env `AGENTIC_OS_NOTIFY_CMD`
      (a LOCAL subprocess, `shell=True`); payload delivered on STDIN + env vars
      `AGENTIC_OS_NOTIFY_{EVENT,GOAL,STATE,SUMMARY,PAYLOAD}`. Whole invocation wrapped
      (missing/nonzero/hanging never aborts a goal; `DEFAULT_NOTIFY_TIMEOUT_SEC=15`
      cap). Payload routed through the P2 `scrub_secrets()` before it reaches the hook
      or the run-log; a `notify` run-log line is always recorded (even with no hook).
    - `FRAMEWORK_VERSION` 0.4.0 → 0.5.0; parser description mentions P4.
  - `tests/test_p4.py` (new): 61 checks, OP1–OP4 + BP (no GUI/dashboard, gate framed
    anti-drift, notify+follow wired) on throwaway git repos (auto-cleaned). Uses the
    mock runner + `crash_after_iteration` (OP1 live-update proof via crash→read→
    resume→read) + a notifier that appends to a sink read from `NOTIFY_SINK`.
  - `docs/OBSERVABILITY.md` (new) + `docs/ORCHESTRATOR.md` (P4 now built, not out-of-scope).
- **Why:** satisfy OP1–OP4. Reused existing machinery per the ladder — the per-iteration
  `flush()` already wrote status live (OP1 just needed clean glanceable fields + a proof);
  `scrub_secrets()` (P2) is the notify scrub (B4); `_append_runlog` already scrubs; the
  mock `crash_after_iteration`/`gamed_pass`/`agent_stop_after`/`note` affordances drive all
  four events + the scrub test offline.
- **Verify (run yourself):** `python tests/test_p4.py` → 61/61 ALL PASS; regression
  `python tests/test_p{0,1,2,3}.py` → 53/82/64/64 unchanged. Manual e2e: a 3-iteration
  mock success fired EXACTLY ONE `finish` notify to a real hook sink; `status` showed the
  AT A GLANCE line; run-status.json carried state/active_goal/active_iteration/agg/criteria/
  tokens/budget.
- **Next iteration should know:** two test FAILs on first run were TEST-side false positives
  (fixed, product was correct): (1) the real-secret scanner tripped on the JSON-escaped
  redaction mark `[REDACTED]\"` in the sink — fixed to `.startswith("[REDACTED]")`;
  (2) BP5 substring check tripped on the doc's own negated phrase "NOT a security or
  correctness guarantee" — fixed to a positive-claim regex. `_glance_line` shows
  `criteria=0/0` when a goal has no rubric (fine; tests attach a valid rubric to get 1/2).
  Not committed by me yet at time of writing — see final step. Verifier decides done, not me.

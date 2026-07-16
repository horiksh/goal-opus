# Progress log — <goal slug>

Maker handoff memory. One entry per iteration, appended by goal-maker.
The verifier never reads this file.

---

## Iteration N — <yyyy-mm-dd>
- **Changed:** <what and where>
- **Why:** <reason, tied to failing criteria ids>
- **Next iteration should know:** <gotchas, partial work, dead ends>

---

## Iteration 1 — 2026-07-15
- **Changed (all in `D:\horil\agentic-os`, committed there; FRAMEWORK_VERSION 0.5.0 -> 0.6.0):**
  - `cli/agentic_os.py`:
    - **LP1** — added `encoding="utf-8", errors="replace"` to ALL 11
      `subprocess.run(text=True)` calls (claude + git + rubric_check + notify).
    - **LP2** — `_git_checkpoint(..., product_paths=)` now also stages the maker's
      REPORTED `files_changed` (threaded via `IterationOutcome.files_changed` ->
      `GoalCtx.changed_files` -> finalize), so a real created/edited product file
      lands in the checkpoint and `undo` reverts it. Deliberately selective
      (reported paths that exist within target only) — NOT a blind `git add -A` —
      so BP4/BP7 still refuse over a SEPARATE unreported user file. Mock path
      unchanged (no product paths -> only STATE.md + `.agentic-os/` staged).
    - **LP3** — `_consume_goal()` marks a completed goal `consumed` in
      `.agentic-os/queue.json` at finalize (states in `_CONSUMING_STATES` =
      success/flagged/aborted/no-progress/declined; NOT stopped/held);
      `RealRunner.queue()` filters consumed goals so a later run/resume never
      re-runs them. Mock reads the fixture (not the queue) -> inert there.
    - **LP4** — `cmd_resume` now CONTINUES after an `AGENT_STOP` halt: a
      `session_end` state `stopped` with pending goals is resumable (not a no-op);
      it runs the pending goal(s), never re-running completed ones. Added budget
      INHERITANCE (real-mode resume with no `--iteration-budget` inherits the
      halted session's own budgets from run-status) so continue-after-halt is not
      refused as unbounded. `_reconstruct_session` now reports `end_state`/`halted`.
    - **LP5** — `_invoke_claude` guards None/empty/undecodable/no-JSON claude
      output -> raises a clean per-iteration `OrchestratorError` (caught by
      cmd_run/cmd_resume) instead of a raw `TypeError('NoneType' not iterable)`.
      `_parse_last_json(None|"")` now raises OrchestratorError, not TypeError.
  - `docs/ORCHESTRATOR.md` + `docs/DURABILITY.md` — documented the
    continue-after-halt verb (`resume`; `run` also continues) + queue consumption.
  - `tests/fixtures/fake_claude_stub.py` — the FAKE-CLAUDE STUB substrate: emits a
    real-shaped envelope with a NON-ASCII (U+2019) fenced `result` and a maker turn
    that CREATES a real product file; maker/verifier decided by a persistent call
    counter (argv-independent, so cmd.exe never parses the metachar prompt).
  - `tests/test_p9.py` — LP1–LP6 (54 checks) driving the REAL runner via the stub.
- **Why:** fixes the 5 mock-hidden §8 integration bugs (FINDINGS.md) so the real
  runner works end-to-end on this cp932 box.
- **Verified:** `python tests/test_p9.py` -> 54/54 ALL PASS. Regression:
  P0 53/53, P1 82/82, P2 64/64, P3 64/64, P4 61/61, P8 30/30 (all unchanged).
- **Next iteration should know:**
  - The stub is invoked as `claude.cmd` (Windows) / `claude` (POSIX) with NO argv
    forwarding — it uses a call COUNTER in `STUB_STATE_DIR` (kept OUTSIDE the
    target so it never pollutes the checkpoint). Odd calls = maker, even = verifier.
  - `run` also continues after a halt (queue consumption); `resume` is the
    documented canonical verb (matches §8 wording).
  - For the §8 re-run: the checkpoint stages ONLY the maker's REPORTED files. If
    the §8 driver leaves install/setup artifacts UNTRACKED at undo time, undo will
    still (correctly) refuse over them — the driver should commit setup to base so
    only the maker's delta is uncommitted (this is a driver/setup concern, not a
    product bug).

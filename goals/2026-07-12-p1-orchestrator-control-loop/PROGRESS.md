# Progress log — 2026-07-12-p1-orchestrator-control-loop

Maker handoff memory. One entry per iteration, appended by goal-maker.
The verifier never reads this file.

---

## Iteration 1 — 2026-07-12
- **Changed (all in TARGET `D:\horil\agentic-os`, committed there):**
  - `cli/agentic_os.py` — EXTENDED the P0 CLI with the P1 orchestrator (one file,
    no new binary): the §4d control loop `_control_loop`, `MockRunner` + `RealRunner`
    behind one loop, `GoalCtx`/`IterationOutcome`, rubric gate `_gate_rubric` (delegates
    to the target's `tools/rubric_check.py`, framework copy as fallback), budget resolution,
    STATE.md/run-log/run-status/git-checkpoint write-back, and 7 new verb handlers wired into
    `build_parser` (`enqueue-goal/run/status/pause/steer/resume/undo`). Bumped FRAMEWORK_VERSION
    to 0.2.0.
  - `tests/test_p1.py` — NEW, 82 checks over throwaway git repos in the scratchpad (all mock
    mode), one section per QP1–QP8 + a BP8 source-inspection check. `tests/test_p0.py` untouched
    (still 53/53).
  - `docs/ORCHESTRATOR.md` — NEW P1 design doc (loop, states, sentinels, budgets, verbs, mock
    handle); `README.md` status + verb table + quickstart; `STATE.md` verified facts + Last session.
- **Why (criteria):** QP1 rubric gate (refuse invalid/no-max_iterations, valid still runs);
  QP2 per-goal `max_iterations` abort (exactly N iterations, distinct `aborted`); QP3 token +
  aggregate-iteration budgets each stop the session, cumulative surfaced, no-budget refused
  (exit 2); QP4 ≥2 goals sequenced single-threaded with STATE.md+run-log+git-checkpoint write-back
  per run (judged from `run-status.json` + `run-log.jsonl` + `git log`); QP5 empty queue → idle
  exit 0 (subprocess timeout guards against spin); QP6 AGENT_STOP halts within one iteration +
  write-back, STEER.md folded once then deleted; QP7 no-progress → distinct terminal state (< max_iters);
  QP8 verb surface --help exit 0 + names verb, enqueue→status legible, unknown verb non-zero,
  resume/undo documented P2/P3 stubs. BP8: real path is the DEFAULT (RealRunner) and constructs
  maker/verifier packets + invokes `claude` — mock is the opt-in branch.
- **Key design calls:**
  - Loop granularity = ONE goal-opus ITERATION per loop step (not a whole goal) — required so
    sentinels are polled per iteration (QP6 "halt within one iteration") and per-goal `max_iterations`
    is counted by the orchestrator (QP2).
  - Session top-level `state` = the last goal's terminal state on drain (or `idle` if nothing ran,
    `aborted` on budget, `stopped` on AGENT_STOP). Per-goal states live in `run-status.goals[]` +
    run-log `goal_end` events. This makes QP2/QP7 "state=aborted/no-progress" and QP5 "state=idle"
    all true from one field without conflating scopes.
  - No-progress detector keys off `changed=false` (default `changed=true`), NOT `outcome`, so an
    `abort` goal (changed=true) runs to `max_iterations` and does NOT prematurely trip no-progress.
    IMPORTANT for anyone writing fixtures: keep `changed:true` on abort goals.
  - Mock affordance `agent_stop_after:N` lets a fixture drop AGENT_STOP mid-goal deterministically
    (that's the whole point of the mock) — pre-creating AGENT_STOP would halt before any iteration.
  - No-budget REFUSAL reachability: a bare-list mock fixture gets an ergonomic default iteration
    budget (stays bounded); an object fixture with `budgets:{iteration_budget:null,token_budget:null}`
    keeps both None → refused (QP3c). Real runs have no ergonomic default → refused if unconfigured.
- **Next iteration should know:** All 82 P1 + 53 P0 checks pass locally (Windows, `python`
  pinned via `sys.executable`; git via `git -C`). Verify commands: `python tests/test_p1.py`
  and `python tests/test_p0.py` from `D:\horil\agentic-os`. Runtime artifacts land under the
  TARGET's `.agentic-os/` (never the home). Scope held to P1: `resume`/`undo` are declared stubs;
  no crash-resume, secret-scrub, undo, or push-notify built (P2/P3/P4). Work committed in the
  agentic-os repo; home carries only this workdir.

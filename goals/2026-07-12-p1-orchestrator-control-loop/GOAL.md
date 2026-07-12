# GOAL — agentic-os P1 (Orchestrator control loop, PRD §4d)

## Goal statement
Build **Phase P1 (Orchestrator control loop)** of the agentic-os PRD
(`prds/2026-07-09-agentic-os/PRD.md` §4d, §7): a **single-active-TARGET** bounded, resumable
control loop (`agentic-os run`) that sequences goal-opus runs over a shared file-memory goal
**queue** — with a run-lifecycle **state machine**, control **sentinels** (`AGENT_STOP`,
`STEER.md`), hard **iteration + token budgets**, a **no-progress** detector, a clean
**empty-queue idle** exit, and the operator **verb surface** (enqueue-goal / run / status /
pause / steer). Closing gate (PRD §7): two goals run end-to-end, states transition correctly,
`max_iterations`+token budget enforced (B3), kill-switch halts mid-run, empty-queue exits clean.

Scope is **strictly P1**. Out of scope (later phases): guaranteed crash write-back + idempotent
resume (P2), secret-scrub/export/size-warning (P2), rollback/undo + land-gate + classifier-decline
branch (P3), tailable status polish + push notify (P4), concurrency/fan-out (deferred §3). The
`resume` and `undo` verbs may be **declared/stubbed** (routing to their future phase) but are not
built or verified here.

## TARGET
`D:\horil\agentic-os` (P0 head `ca5a3fa`, private remote `origin`). P1 EXTENDS the P0 CLI
(`cli/agentic_os.py`) — same repo, same self-contained framework. All product code lands here;
the home receives only run evidence (`goals/2026-07-12-p1-orchestrator-control-loop/`) + memory.
Product/evidence in the home = banned outcome BP1.

## Requirement coverage (PRD §4b / §7 / master seed)
Master-seed criteria mapped to P1: **C1** (rubric gate), **C3** (bounded), **C6** (sequence ≥2
goals), **C7** (sentinels). Reqs: **U3** (empty-queue idle), **U11** (sentinels), **U12**
(aggregate budget), **U13** (token budget + surfacing), **U15** (no-progress), **U34** (verb
surface), plus the **§4d** state machine (`idle → running → {paused | no-progress | success |
aborted | crashed}`). Carried banned outcomes: **B1**, **B3**, **B5**, **B9**.

## Key design decisions (my Phase-1 calls — flag at sign-off if you disagree)
1. **Deterministic test mode is mandatory (how the control loop is verified).** The orchestrator
   must expose a documented mock/test handle — env `AGENTIC_OS_MOCK_RUNNER=<fixture.json>` — where
   the fixture scripts each queued goal's outcome (`success|abort|no-progress|decline`), iteration
   count, token cost, and whether it changed anything. In mock mode the control loop runs its FULL
   machinery (state transitions, budgets, sentinels, run-log, git checkpoints, write-back) using
   these scripted outcomes **instead of live maker/verifier agents**. This makes every P1 criterion
   deterministically executable without burning LLM tokens or being non-deterministic — the loop's
   own outputs are real; only the goal *content* is mocked. (Mirrors P0's `AGENTIC_OS_NO_JUNCTION`
   test switch.)
2. **The real (non-mock) run path must exist and be the DEFAULT.** `agentic-os run` without the
   mock env drives a real goal-opus iteration (constructs maker/verifier packets and invokes the
   loop). The mock is opt-in for testing only. A mock-ONLY implementation with no real integration
   seam is a banned outcome (BP8). The real path's *robustness under live LLM load* is hardened at
   final acceptance (§8), not gated here — P1 gates the **control flow**.
3. **Budgets = per-goal `max_iterations` (C3) AND orchestrator-level aggregate-iteration + token
   budgets (U12/U13), each an independent stop condition** with cumulative spend surfaced in the
   run-status. A run configured without both an iteration bound and a token budget is refused (B3).
4. **Single-threaded** (U14/§3): exactly one active goal writes shared memory at a time; concurrent
   shared-memory writes are banned (BP7/B9).
5. **§4d is `[D]` design with no research backing** — P1 IS its proving ground; expect this phase
   may take >1 iteration (and it's the natural candidate to clear promotion-gate D2 item 2, "one
   real multi-iteration goal").

## Deliverable type
**Non-visual** (CLI + files + control loop). Vision-verify N/A.

## Run mode
Attended — user said "go"; rubric sign-off precedes making. `max_iterations` (this P1 run) = 6.

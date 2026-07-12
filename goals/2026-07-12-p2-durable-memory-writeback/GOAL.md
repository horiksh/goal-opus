# GOAL — agentic-os P2 (Durable memory & write-back)

## Goal statement
Build **Phase P2 (Durable memory & write-back)** of the agentic-os PRD
(`prds/2026-07-09-agentic-os/PRD.md` §7): make the orchestrator's memory **durable and
safe** — a **guaranteed write-back on every outcome including a crash** (U32), **crash-mid-run
resumability** from the last checkpoint (U30) with **idempotent replay** (no double write-back /
no re-flipped criteria, U31), a **structural secret-scrub** so no secret ever lands in memory/
STATE.md/run-log/file-messages (U21), a **memory export/backup** (U6), an explicit **redaction/
scrub path** (U7), and a **size-threshold consolidation warning** (U5, manual — automated
"dreaming" stays deferred). Closing gate (PRD §7): crash mid-run → resume without double-apply
(U30/U31); secrets scan clean (B4); write-back present on every outcome (B7).

Scope is **strictly P2** (durability + memory hygiene, built ON TOP of P1's control loop). Out of
scope (later): rollback/undo + land-gate + classifier-decline branch (P3), observability polish +
push notify (P4), concurrency (deferred §3). No new run backend — P2 hardens P1's write-back/
resume path; the P1 `AGENTIC_OS_MOCK_RUNNER` substrate is reused (extended with a crash affordance).

## TARGET
`D:\horil\agentic-os` (P1 head `1a5641b`, private remote `origin`). P2 EXTENDS the same
`cli/agentic_os.py` (checkpoint/journal/write-back, resume, scrub, export, size-warning) — same
self-contained framework. All product code here; the home receives only run evidence +
memory. Product/evidence in the home = banned outcome BP1.

## Requirement coverage (PRD §4b / §7 / master seed)
Master-seed criteria mapped to P2: **C2** (write-back on every outcome incl crash), **C4** (no
secrets in memory/state/logs), **C8** (crash resume idempotent). Reqs: **U5** (size-threshold
warning), **U6** (export/backup), **U7** (redaction/scrub path), **U10** (run log — already shipped
in P1, resume rehydrates from it), **U21** (pre-write secret guard), **U30** (crash resumability),
**U31** (idempotent replay), **U32** (guaranteed write-back on crash/cancel). Carried banned
outcomes: **B1, B4, B5, B7**.

## Key design decisions (my Phase-1 calls — flag at sign-off if you disagree)
1. **Durability = incremental idempotent journaling, not a final flush.** A SIGKILL can't run a
   handler, so "guaranteed write-back on crash" must come from writing the run-log/checkpoint/state
   BEFORE and AFTER each step so a crash always leaves a durable, resumable record; on `resume` the
   orchestrator detects the partial run and completes/continues without re-doing finished steps.
   Every write-back step is idempotent (keyed by goal+iteration) so replay never double-applies.
2. **Deterministic crash handle (mandated, extends the P1 mock).** The mock fixture gains a per-goal
   `crash_after_iteration: N` that makes the process terminate ABRUPTLY (non-graceful, no clean
   shutdown, e.g. `os._exit`) after step N — simulating a real crash — so resume/idempotency criteria
   are deterministically testable. A writeback-content field (e.g. `note`) lets tests route a known
   secret into the write-back path to prove the pre-write scrub redacts it.
3. **Secret hygiene has TWO paths:** a **pre-write guard** (U21 — scrub before anything is written to
   memory/log/message) AND an after-the-fact **redact/scrub command** (U7 — clean existing memory).
   Both verified.
4. **Export + scrub are LOCAL plain-file/git operations** (U6) — no network (a banned outcome).
5. **Size warning is a WARNING only** (U5) — surfaced, manual; automated consolidation ("dreaming")
   stays deferred per PRD §3.

## Deliverable type
**Non-visual** (CLI + files + durability mechanics). Vision-verify N/A.

## Run mode
Attended — user invoked `/goal-opus P2`; rubric sign-off precedes making. `max_iterations` = 6.

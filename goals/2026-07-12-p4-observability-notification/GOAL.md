# GOAL — agentic-os P4 (Observability & notification)

## Goal statement
Build **Phase P4 (Observability & notification)** of the agentic-os PRD
(`prds/2026-07-09-agentic-os/PRD.md` §7): make a running session **glanceable and
push-aware** — a **tailable, machine-readable run-status** (U9) that updates live and a
**compact at-a-glance human summary**, plus a **minimal PUSH notification** (U35) fired on the
notable terminal/blocking events (**finish / block / budget / decline**). Closing gate (PRD §7):
the operator reads status **at a glance** AND is **notified** on finish/block/budget/decline.

Scope is **strictly P4** (observability + notification, on top of P0–P3). **No status DASHBOARD/GUI**
— PRD §7 is explicit that a dashboard would be a UI slice requiring `/design-direction` first; P4's
"at a glance" is a compact TEXT view, not a visual surface. Out of scope: concurrency (§3). No new
run backend — P4 extends the P1–P3 orchestrator's existing `run-status.json` / `status` verb and the
event stream; the `AGENTIC_OS_MOCK_RUNNER` substrate is reused.

## TARGET
`D:\horil\agentic-os` (P3 head `f2d0193`, v0.4.0, private remote `origin`). P4 EXTENDS the same
`cli/agentic_os.py` (tailable status polish + a push-notify hook). All product code here; the home
receives only run evidence + memory. Product/evidence in the home = banned outcome BP1.

## Requirement coverage (PRD §4b / §7)
Reqs: **U9** (machine-readable tailable run-status: iteration, criteria pass count, tokens) — partly
shipped in P1 (`run-status.json` + `status`); P4 adds live tailability + the at-a-glance view.
**U35** (push notification on finish/block/budget/decline — not just pull). No NEW master-seed
criterion is dedicated to P4 (C1–C12 have no observability criterion; U9/U35 are the reqs). Carried
banned outcomes: **B1, B4** (a notification is a file-message → must be secret-scrubbed), **B5**.

## Key design decisions (my Phase-1 calls — flag at sign-off if you disagree)
1. **Push = a configurable notify-command hook.** The genuinely-push, portable, local, testable
   primitive is env `AGENTIC_OS_NOTIFY_CMD` — the orchestrator ACTIVELY invokes it with the event
   payload on finish/block/budget/decline. (The framework MAY ship a default, e.g. a Windows toast
   one-liner, but the hook is the mechanism.) This is "push" (orchestrator-initiated), not a file the
   user must poll — and it needs no network.
2. **Notify is OPTIONAL and NON-FATAL.** No configured command → the run still completes. A notify
   command that fails/exits-nonzero → the run still completes (a notification failure must never
   abort a goal). — banned outcome BP2.
3. **The notification payload is SCRUBBED.** A push notification is a file-message (PRD B4), so it
   goes through the P2 pre-write secret scrub — no secret in a notification. — banned outcome BP4.
4. **"At a glance" is a compact TEXT view, NOT a GUI/dashboard** (a dashboard would need
   `/design-direction`; explicitly out of P4). Tailability = live per-iteration updates the operator
   can `--follow`/tail.

## Deliverable type
**Non-visual** (CLI + files + text status + push hook). Vision-verify N/A (and a dashboard is
explicitly out of scope — no design-direction anchor needed).

## Run mode
Attended — user invoked `/goal-opus P4`; rubric sign-off precedes making. `max_iterations` = 5.

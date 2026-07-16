# GOAL — agentic-os P9 (Live-hardening: fix the 5 §8 integration bugs)

## Goal statement
Fix the five real integration bugs the full live §8 surfaced (all mock-hidden), so the agentic-os
real runner actually works end-to-end on this (cp932/Japanese-Windows) machine with real product
changes — then the full live §8 can pass. Bugs (evidence:
`goals/2026-07-13-p8-real-runner-hardening/reports/live-s8-full/FINDINGS.md`):
1. **[high] UTF-8** — every `subprocess.run(..., text=True)` lacks `encoding="utf-8"` → on cp932 a
   non-ASCII byte in claude/git output (0x92, a curly quote) → `UnicodeDecodeError` → `NoneType` crash.
2. **[high] Checkpoint doesn't stage product changes** — `git add STATE_REL AO_DIR` only, so the
   maker's real files are untracked, absent from the checkpoint → `undo` can't revert a real change
   (U33/B11 broken for real diffs); BP7 then refuses over the untracked files.
3. **[med] Queue not consumed** — `run` re-runs completed goals (not dequeued).
4. **[med] resume-after-halt no-op** — after an AGENT_STOP halt, `resume` treats stopped as terminal
   and doesn't continue the pending goal.
5. **[low] No None-guard** — a failed claude decode → confusing `TypeError` instead of a clean error.

## TARGET
`D:\horil\agentic-os` (v0.5.0, head `3415448`). All product code here. Home gets evidence + memory.

## Key design decisions (my Phase-1 calls — flag at sign-off if you disagree)
1. **A FAKE-CLAUDE STUB is the deterministic-but-faithful test substrate for the real runner.** The
   mocks hid these bugs because they never spawn a subprocess, never emit non-ASCII, never create real
   files. P9 introduces a fake `claude` stub (a local script placed on a temp PATH) that emits a
   REAL-SHAPED envelope (with the real key set + a markdown-fenced `result`) **containing non-ASCII
   bytes** AND **actually creates a product file** in the target. This drives the REAL runner path
   (unwrap, decode, usage, checkpoint, undo) DETERMINISTICALLY — closing the exact gap that let bugs
   1+2 hide. (This is the real-runner analogue of the AGENTIC_OS_MOCK_RUNNER substrate.)
2. **Checkpoint stages the maker's changes** (fix #2): the checkpoint captures the working-tree delta
   the goal produced (e.g. `git add -A`) so the product change IS in the commit and `undo` reverts it;
   after a clean checkpoint the tree is clean so undo doesn't hit the BP7 untracked refusal. **BP7 must
   still hold** — undo refuses over genuinely-uncommitted USER work that the checkpoint didn't stage.
3. **Continue-after-halt** (fix #4): after an AGENT_STOP halt with pending goals, continuing (via
   `resume` per §8's wording, and/or `run`) processes the PENDING goal WITHOUT re-running completed
   ones (depends on fix #3). Maker picks the coherent semantics and documents it; the §8 re-run uses it.
4. **Least-privilege + secret-scrub + mock path all preserved** (no regression to P0–P4/P8).

## Deliverable type
**Non-visual** (CLI hardening + tests + docs). Vision-verify N/A.

## Run mode
Attended — user chose "P9 live-hardening, then re-run §8". Rubric sign-off precedes making (proceed
unattended if not returned, per protocol). `max_iterations` = 5 (substantial; may finally go
multi-iteration). After P9 passes, the orchestrator re-runs the FULL live §8.

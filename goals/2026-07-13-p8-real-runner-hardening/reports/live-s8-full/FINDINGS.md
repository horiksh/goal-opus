# Full live §8 acceptance — 2026-07-13 — VERDICT: DOES NOT PASS

The full §8 script (2 live goals + live AGENT_STOP + resume + undo + run-again) surfaced a
CLUSTER of real integration bugs, ALL hidden by the deterministic mocks (P0–P4) AND by the
ASCII-only one-goal smoke. This is the "MOCK-VERIFIED ≠ LIVE-READY" lesson, at full force.

WHAT WORKED (live):
- Real goal core: g1 ran maker→verifier→gate→writeback live (checkpoint 3083726, 2051 tokens).
- Live AGENT_STOP mid-run halt: dropped during g1's live turn → g1 completed & landed, g2 NEVER
  started, state=stopped. (The kill-switch works with the real runner.)

BUGS FOUND (live, mock-hidden):
1. [SEV: high] ENCODING — every `subprocess.run(..., text=True)` (incl. _invoke_claude L1207, and
   the git/rubric_check calls) lacks `encoding="utf-8"`. On this cp932 (Japanese Windows) locale,
   claude's output containing byte 0x92 (a curly quote) → UnicodeDecodeError in the reader thread →
   stdout=None → downstream `TypeError: 'NoneType' object is not iterable`. Real runs crash on any
   non-ASCII model/git output. FIX: pass encoding="utf-8" (+ errors="replace") to every text=True
   subprocess.run.
2. [SEV: high] CHECKPOINT DOES NOT STAGE PRODUCT CHANGES — the checkpoint does `git add STATE_REL
   AO_DIR` only, so the maker's real product file (alpha.txt) is UNTRACKED, absent from the commit.
   Therefore `undo` cannot revert a real autonomous change (U33/B11 don't hold for real diffs); and
   BP7 (correctly) refuses to reset over the untracked files. The mock never exposed this because
   mock "changes" were STATE.md rows that the checkpoint's `git add STATE_REL` did capture. FIX:
   the checkpoint must stage the maker's changes (git add -A, or add the reported files_changed).
3. [SEV: med] QUEUE NOT CONSUMED — `run` again re-runs completed goals (g1 goal_start seen twice);
   a completed goal is not dequeued. FIX: mark/skip completed goals in the queue.
4. [SEV: med] RESUME-AFTER-HALT NO-OP — after an AGENT_STOP halt (state=stopped), `resume` treats
   the session as terminal and no-ops (does NOT continue g2). §8 expects "resume continues"; either
   resume must continue-after-stop, or the product must document that `run` continues the queue
   (but see bug 3). Needs a semantics decision.
5. [SEV: low] No None-guard on the agent report after a failed claude decode (cascades bug 1 into a
   confusing TypeError instead of a clean per-iteration error).

RECOMMENDATION: a focused P9 "live hardening" effort (or its own PRD phase) addressing 1–5, then
re-run the full live §8. Bugs 1 and 2 are the load-bearing ones.

# PRD §8 FINAL ACCEPTANCE — PASS (live, end-to-end) — 2026-07-13/15

After P9 live-hardening, the FULL live §8 acceptance script passed end-to-end against real
`claude` (C:\Users\horil\.local\bin\claude.exe), verified TWO independent ways.

## The run (real claude, sandboxed throwaway target, AGENTIC_OS_DANGEROUSLY_SKIP_PERMISSIONS=1)
- Fresh `agentic-os init` + a bootstrap commit + `enqueue-goal` x2 (g1=alpha.txt, g2=beta.txt), each
  with a Default-FAIL rubric.
- `run` bounded (iteration + token budget): g1 ran a live maker→verifier→gate→write-back loop and
  landed (checkpoint 5be63b5, 1895 tokens).
- LIVE `AGENT_STOP` dropped during g1's real turn → halted within one iteration: g1 landed, g2 NEVER
  started, state=stopped.
- `resume` → continued g2 WITHOUT redoing g1 (g1 goal_start stays 1); g2 landed (checkpoint a6c86d7,
  2442 tokens); session=success. Total 4337 real tokens across 2 goals.
- `undo` → reverted the last landed change: HEAD a6c86d7 → 5be63b5 (g2's recorded pre-change SHA),
  beta.txt GONE, alpha.txt KEPT; the undone g2 checkpoint recoverable via git reflog (non-destructive).

## Two-way verification (both PASS)
(a) Replay from status file + git log reproduces the final state (state=success pre-undo; post-undo
    HEAD at g1's checkpoint; reflog preserves g2). 
(b) Fresh-context goal-verifier, given ONLY artifacts (git history/reflog + .agentic-os/ + working
    tree, NO orchestrator narration), confirmed all 5 claims — 2 goals + per-goal write-back,
    sequenced/single-threaded/shared-memory, AGENT_STOP halt, resume-without-redo, undo reverts —
    overall PASS. It recovered the pre-undo run-log (halt/session_end=stopped/session_resume events)
    from the g2 checkpoint's committed blob, so the full history is preserved in git even though undo
    reverted the on-disk .agentic-os/.

## Note (not a failure)
`undo` (git reset to the pre-change SHA) also reverts `.agentic-os/`, so the on-disk run-log/status
after an undo reflect the pre-undone state; the full audit trail lives in git (the undone checkpoint's
committed run-log blob + reflog). A future refinement could keep an on-disk audit trail across undo,
but git already preserves everything recoverably.

## Bottom line
The agentic-os v1 (P0-P4 core + P8 real-runner + P9 live-hardening) now passes its PRD §8 final
acceptance LIVE, end-to-end, verified two ways. v1 is DONE.

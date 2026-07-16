# Progress log — <goal slug>

Maker handoff memory. One entry per iteration, appended by goal-maker.
The verifier never reads this file.

---

## Iteration 1 — 2026-07-12
- **Changed:** Extended `D:\horil\agentic-os\cli\agentic_os.py` (P3 safe autonomy),
  added `docs\SAFE-AUTONOMY.md` + `tests\test_p3.py`, updated `docs\ORCHESTRATOR.md`
  + `docs\DURABILITY.md`. Committed in the TARGET at `3148662` (branch `main`,
  following the P0/P1/P2 convention of committing phase work to main). Bumped
  FRAMEWORK_VERSION 0.3.0 -> 0.4.0.
- **Why (per criterion):**
  - **SP1 (undo):** `finalize` now captures the pre-change SHA at land time and
    pushes it onto `.agentic-os/undo-log.json` (also surfaced in run-status +
    a `land_gate` run-log event). Real `cmd_undo` replaces the P1 stub: it
    `git reset --hard`s HEAD back to that SHA. Undo-log lives under the checkpoint
    so the reset self-maintains the stack.
  - **SP1/BP7 (safety):** `_git_user_changes` excludes `.agentic-os/` churn;
    `undo` REFUSES on any other uncommitted change (`--force` overrides). NEVER a
    blind reset over user work.
  - **SP2 (land-gate):** `IterationOutcome.evidence_ok` + mock `gamed_pass`
    affordance. A success with `evidence_ok=False` finalizes to `flagged` (not
    `success`), still checkpointed+undo-pointered so it is reversible.
  - **SP3 (approve-before-land):** `run --approve-before-land` / env toggle. Enabled
    -> `held` (no checkpoint, HEAD unchanged, pending-approval.json); `approve` verb
    lands it later with an undo pointer. Disabled -> lands as `success`.
  - **SP4 (decline):** strengthened the existing decline branch into a
    fallback/human escalation event `{disposition, retried:false, is_error:false}`;
    goal finalizes `declined`, exactly one iteration, no re-issue.
  - **SP5 (least-privilege):** verifier already read-only (`Read,Glob,Grep,Bash`) —
    left untouched. `_claude_permission_flags` gates `--dangerously-skip-permissions`
    behind an explicit opt-in env (never blind). `docs\SAFE-AUTONOMY.md` documents
    the prefix-deny-is-bypassable caveat + frames the gate as anti-drift not security.
- **Evidence:** `python tests/test_p3.py` -> 64/64 ALL PASS; test_p0 53/53, test_p1
  82/82, test_p2 64/64 all still green (no regression). Raw CLI end-to-end for
  SP1/SP2 confirmed HEAD==pre-change SHA after undo.
- **Next iteration should know:**
  - All P3 criteria are mock-based; `new_repo_committed` in test_p3 makes an initial
    commit so a real pre-change SHA exists (throwaway repos from git-init alone have
    an unborn HEAD — undo records `pre_change_sha=None` and refuses).
  - Kept `_git_checkpoint` staging `STATE.md + .agentic-os/` (unchanged) — did NOT
    switch to `git add -A`, to avoid P1/P2 risk. In the mock, product == orchestrator
    state, so this is correct; real-path product-staging breadth is a PRD-8 concern.
  - test_p1 `test_qp8` asserts `undo` output contains "P3" and exits 0 on a repo with
    no landing — the real `undo` preserves that (nothing-to-undo -> exit 0, mentions
    "P3 · Safe autonomy"). Do not remove that phrase.

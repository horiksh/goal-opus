# Progress log — <goal slug>

Maker handoff memory. One entry per iteration, appended by goal-maker.
The verifier never reads this file.

---

## Iteration N — <yyyy-mm-dd>
- **Changed:** <what and where>
- **Why:** <reason, tied to failing criteria ids>
- **Next iteration should know:** <gotchas, partial work, dead ends>

---

## Iteration 1 — 2026-07-13
- **Changed:** all in TARGET `D:\horil\agentic-os` (committed there; home only gets this log):
  - `cli/agentic_os.py`:
    - NEW pure `_extract_agent_report(stdout_or_envelope) -> dict` (after `_parse_last_json`):
      parses the `claude -p --output-format json` ENVELOPE, takes `result` (a STRING),
      re-runs the balanced-brace scan ON that fenced/prose string to pull the INNER report.
      Accepts raw stdout text OR a pre-parsed dict; a bare report (no envelope) is returned
      unchanged (mock/test robust). [HP1]
    - `_invoke_claude` now returns `(inner_report, envelope)` — parses the envelope once,
      unwraps the report, and hands the envelope back so the caller can count tokens.
      (Kept `def _invoke_claude`…`def _parse_last_json` adjacency so test_p3's source-slice
      guard on the permission flags still holds.)
    - `_usage_tokens(envelope)` rewritten: sums `usage.input_tokens + usage.output_tokens`
      (the real envelope has NO `total_tokens`); falls back to a bare `total_tokens` shape and
      to 0. [HP2]
    - `RealRunner.run_iteration`: consumes the tuple; counts tokens from BOTH the maker and
      verifier ENVELOPES.
    - `cmd_run`: run-start PREFLIGHT — real mode only, `shutil.which("claude") is None` →
      print "claude not found" to stderr and `return 1` BEFORE `_control_loop` (so no
      run-status / journaling / stale `state=running`). Mock mode skips it. [HP3]
  - `docs/ORCHESTRATOR.md` + `docs/SAFE-AUTONOMY.md`: documented the run-start preflight, the
    envelope-unwrap/usage shape, and that a LIVE run needs the maker granted WRITE via the
    `AGENTIC_OS_DANGEROUSLY_SKIP_PERMISSIONS` opt-in OR a `.claude/settings*.json` allowlist
    (least-privilege preferred; skip stays env-gated, OFF by default). [HP4]
  - `tests/fixtures/real_claude_envelope.json`: genuine captured envelope copied byte-identical
    from the goal fixture (real keys + fenced `result`; BP2 — no hand-built stub).
  - `tests/test_p8.py`: new suite (30 checks) grading HP1–HP5 against the real fixture.
- **Why:** §8 gap — `_invoke_claude` returned the ENVELOPE (never unwrapped `result`) so
  `files_changed`/`evidence`/`overall` read empty; `_usage_tokens` read a nonexistent
  `total_tokens` → 0. Fixes map HP1 (unwrap), HP2 (usage), HP3 (preflight), HP4 (perm docs),
  HP5 (no regression).
- **Verified:** `python tests/test_p8.py` → 30/30 ALL PASS; regression `test_p0..p4` →
  53/82/64/64/61 all green (mock path untouched). Committed in TARGET on `main`.
- **Next iteration should know:** the parse/usage criteria are fully deterministic (fixture-
  based, no live claude). The remaining LIVE §8 re-run is the orchestrator's separate step and
  needs claude at `C:\Users\horil\.local\bin\claude.exe` PLUS the write opt-in/allowlist — the
  code + docs are ready for it. `_extract_agent_report` sits AFTER `_parse_last_json`; do not
  move it between `_invoke_claude` and `_parse_last_json` (test_p3 slices that range).

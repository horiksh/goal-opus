# GOAL — agentic-os P8 (Real-runner hardening for live claude)

## Goal statement
Fix the agentic-os REAL runner so it actually works against live `claude -p --output-format json`
— the gap §8 surfaced. Specifically: (1) UNWRAP the CLI result envelope and parse the agent's
report nested (and markdown-fenced) inside `result`; (2) count usage tokens from the ENVELOPE's
`usage` (input+output), not a nonexistent `total_tokens`; (3) add a run-start `which(claude)`
PREFLIGHT so a claude-less real run refuses cleanly BEFORE journaling; (4) document the live-run
permission opt-in the headless maker needs to write files. Then a live §8 re-run (done separately
by the orchestrator) is the real acceptance.

Scope is strictly the real-runner adapter + its docs/tests. Do NOT change the mock path, the
control loop, budgets, sentinels, undo/land-gate, or observability — only the `claude`-turn
adapter (`_invoke_claude` / `_parse_last_json` / `_usage_tokens` / RealRunner) + a run-start
preflight + docs.

## TARGET
`D:\horil\agentic-os` (P4 head — v0.5.0; §8-blocked note in target STATE.md Open failures). All
product code here. Home gets run evidence + memory only (BP1).

## Ground truth (captured real envelope — the deterministic test fixture)
A REAL `claude -p --output-format json` envelope is captured at
`goals/2026-07-13-p8-real-runner-hardening/fixtures/real_claude_envelope.json`. Its shape:
- top-level keys: `type, subtype, is_error, duration_ms, num_turns, result, stop_reason,
  session_id, total_cost_usd, usage, modelUsage, permission_denials, uuid, terminal_reason, ...`
- `result` is a STRING containing the agent's final message. In the capture it is **markdown-fenced
  JSON**: `` ```json\n{"summary":...,"files_changed":["greet.py"],"evidence":[...],"blockers":[]}\n``` ``.
  So extraction must strip the fence / find the JSON object within (reusing the balanced-brace
  `_parse_last_json` on the `result` string works).
- `usage` keys: `input_tokens, output_tokens, cache_read_input_tokens, cache_creation_input_tokens,
  ...` — NO `total_tokens`. Real spend = `input_tokens + output_tokens`.

## The two live-integration bugs (root cause, confirmed by probe)
- `_invoke_claude` returns `_parse_last_json(r.stdout)` = the ENVELOPE (not the inner report) →
  `maker.get("files_changed"/"evidence")` and `verdict.get("overall")` all empty → no real goal passes.
- `_usage_tokens` reads `usage["total_tokens"]` (absent) → 0.
- Minor: `run` journals `iter_begin`/`in_flight` before `which(claude)` → stale `state=running`.

## Key design decisions (my Phase-1 calls — flag at sign-off if you disagree)
1. **Unwrap is a PURE, testable function** (envelope text → inner report dict) separate from the
   subprocess call, so it's graded deterministically against the committed REAL fixture (no live
   claude needed for the parse/usage criteria).
2. **The test fixture MUST be a genuine captured `claude -p` envelope** (BP2), not hand-built — it
   must carry the real envelope keys (session_id, total_cost_usd, modelUsage, cache_* usage) and a
   fenced `result`. The verifier may also re-capture its own real envelope to confirm.
3. **Least-privilege is preserved** (P3): `--dangerously-skip-permissions` stays env-gated
   (`AGENTIC_OS_DANGEROUSLY_SKIP_PERMISSIONS`, default off) — the fix documents that a live run needs
   this opt-in (or a settings allowlist) for the maker to write; it does NOT make it unconditional.
4. **No regression**: P0–P4 suites (53/82/64/64/61) must all still pass; the mock path is untouched.

## Deliverable type
**Non-visual** (CLI adapter + tests + docs). Vision-verify N/A.

## Run mode
Semi-attended — user explicitly chose "fix the runner (P8) then re-run §8", but did NOT return the
Phase-1 rubric sign-off (no answer). Per the protocol's unattended clause, proceeding with the
drafted rubric (rubric_check PASS, coherent, conservative — a focused adapter fix with no-regression
guards). `max_iterations` = 4. After P8 passes, the orchestrator re-runs LIVE §8 (non-deterministic
demo; needs claude at `C:\Users\horil\.local\bin\claude.exe` + the permission opt-in).

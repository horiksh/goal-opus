# Progress log — u1-observatory

Maker handoff memory. One entry per iteration, appended by goal-maker.
The verifier never reads this file.

---

## iter-1 (2026-07-16)

Built the full U1 observatory in the TARGET (D:\horil\agentic-os), stdlib-only
(http.server + vanilla HTML/CSS/JS, no Node/framework/CDN). All 13 criteria
addressed; `python -m pytest tests/test_u1.py -q` = **37 passed**;
`python docs/design/mocks/contrast-check.py` = exit 0 ALL PASS; capture harness
produced all 13 canonical views (self-scored against R3 — see screens/iter-1/).

**What landed (all under the target):**
- `cli/agentic_os.py`: new `dash` verb (`cmd_dash` + subparser). Loopback-only,
  Host-validated, read-only. No forbidden GUI token added to the CLI source
  (kept the P4 BP7 CLI-src check green; UI code lives in `ui/`).
- `ui/server.py`: ThreadingHTTPServer bound 127.0.0.1 ONLY (refuses non-loopback
  bind); `host_header_allowed()` validates every request's Host against the
  localhost allowlist (127.0.0.1/localhost/[::1] + optional :port) → 403 else.
- `ui/reader.py`: torn-read-safe reader (last-known-good in memory), crash
  derivation (in_flight + no session_end), staleness (updated_at vs now),
  non-monotonic % (reads current rubric counts; drop from the UI's OWN observed
  series), skills-card derivation, tokens/forecast, re-redaction via imported
  `scrub_secrets` (with a mirror fallback). READ-ONLY.
- `ui/render.py` + `ui/assets/{tokens.css,app.css,app.js}`: SSR of the C·Helm
  layout (canvas + 2 rails), inlined assets. tokens.css copies the exact
  design-direction hex. app.js polls /api/state, fills EMPTY-at-load ARIA live
  regions (polite/assertive), never steals focus; reduced-motion + theme toggles.
- `ui/fixtures.py`: ONE builder for all 12 canonical views, shared by tests and
  the capture harness. UI observed-% series seeded OUTSIDE `.agentic-os/`.
- `ui/capture_screens.py`: boots the real dash server per view on an ephemeral
  port, drives the design-direction chrome.exe headless command, 1440 + a
  1280-wide home-live (BV10).
- `tests/test_u1.py`: pytest with the exact -k selectors (loopback, host_header,
  torn_read, crash, progress, stale, color_independent, aria, reduced_motion,
  secret, skills, mechanics, read_only).

**Key data-model decisions (for the next iteration):**
- CRASH vs RUNNING: the engine CLEARS `in_flight` between iterations, so a
  healthy running snapshot has `in_flight=None`. Only a PERSISTING `in_flight`
  (+ no session_end) is the crash marker. `home-live` fixture therefore has
  in_flight=None; only `home-crashed` sets it. (Do not "fix" home-live to set
  in_flight — that would falsely read as crashed.)
- The engine `iteration` event carries NO criteria counts, so the DROP
  sparkline/annotation comes from the UI's OWN in-memory series (persisted to a
  UI-owned dir OUTSIDE `.agentic-os/`). `home-live`/`--regressed` seed
  [4/5,3/5] so a single frame shows "▼ dropped 4/5 → 3/5".
- 100%-LANDED requires a land_gate decision=="land" event FOR THE ACTIVE GOAL
  (scoped by goal id — earlier goals' land events must not mark the current
  ring landed).
- Headless Chrome defaults to prefers-color-scheme:LIGHT; captures force theme
  explicitly (`?theme=dark` for all dark views, `?theme=light` for `--light`)
  so `home-live` matches R3's dark canvas.

**Pre-existing (NOT caused by U1, must NOT edit):** `tests/test_p4.py` BP7 has
2 failing checks asserting "P4 ships no .html and no design-direction.md". Both
files are tracked in git HEAD from the earlier design-direction freeze
(726a58f), before U1. I created zero .html files and did not add
design-direction.md; the CLI-src GUI-token check still passes. This is an
obsolete P4-era assertion for the orchestrator to reconcile — the maker is
forbidden from editing engine tests.

---

## iter-2 (2026-07-16) — one focused fix (BV9 light-theme contrast)

Independent verification passed everything except C12, which was tripped by BV9
(text contrast < 4.5:1) on `home-live--light`: two hardcoded, non-token text
colors bypassed the token contract, so `contrast-check.py` (token-only) missed
them.

**Fixed (ui/assets/app.css):**
- `.qrow.active .qnm{color:#fff}` → `color:var(--text)` (+font-weight:600). The
  ACTIVE/running goal NAME was white-on-white (≈1:1, INVISIBLE) on light
  `--surface #FFFFFF`. `--text` is #E8F0F8 in dark (stays bright/emphasized) and
  #0D1622 in light (15.3:1) — now clearly legible in both themes.
- `.lnode.done .lname{color:#cfeed8}` → `color:var(--st-success)`. The completed
  loop-node label was pale-green-on-white (≈1.17:1). `--st-success` is #43C46A
  in dark (7.9:1) and #17752F in light (4.9:1) — legible in both; semantically
  apt (done == success).

**Durable guard (tests/test_u1.py, `-k contrast_hardcode`):**
- `test_contrast_hardcode_no_raw_text_colors_in_css`: scans app.css for any
  `color:` property (negative-lookbehind excludes background-color/border-color/
  stop-color) whose value is not `var(--…)` / a safe keyword → FAILS on any raw
  #hex/rgb text color. This closes the exact hole (token-only checker can't see
  a hardcoded color). contrast-check.py stays as the token-VALUE check.
- `test_contrast_hardcode_guard_would_catch_a_raw_hex`: meta-check proving the
  guard regex flags `#fff` and ignores `background-color:#000`.

**Re-verified:** `grep 'color:#' app.css` = none; `pytest tests/test_u1.py -q` =
**39 passed** (was 37 + 2 guards); `contrast-check.py` = exit 0 ALL PASS.
Re-captured to screens/iter-2/ and Read: `home-live--light.png` — the active
goal name AND the ✓ MAKER done-label are now clearly legible on the light ground
(no text run < 4.5:1); `home-live.png` (dark) — NO regression (active row still
bright/bold, done-label reads as success-green). C12 light-theme BV9 defect
resolved.

---

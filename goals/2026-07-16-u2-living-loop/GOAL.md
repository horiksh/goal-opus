# GOAL — U2 · The living loop (functional motion + flight-recorder + virtualized run-log)

- **Date:** 2026-07-16
- **Slug:** `u2-living-loop`
- **TARGET (all product code lands here):** `D:\horil\agentic-os`
- **Run evidence (this dir):** `D:\horil\agent\goals\2026-07-16-u2-living-loop\`
- **Slice:** PRD §7 **U2** — the second UI slice, extending the U1 read-only
  observatory (`ui/` + the `dash` verb).

## Goal statement (verbatim intent)

Extend the U1 observatory with the three U2 deliverables:

1. **Living-loop MOTION (U31/U32):** the static maker→verifier→land-gate→write-back
   graph gains its **one-shot "you are here" marker transition** on stage change.
   Frozen motion rules apply verbatim (design-direction.md §Motion): functional-only,
   one-shot (NO idle/ambient pulse — that rule was deliberately removed at freeze),
   animation budget = **1 focal at a time**, accent **only** on the single live element
   (BV13), and under `prefers-reduced-motion` the transition is replaced by an **instant
   static color+icon swap** (never deleted).
2. **Flight-recorder timeline (U34):** a scrubbable per-iteration timeline (play / pause /
   step) reconstructed from `.agentic-os/run-log.jsonl` (the append-only journal is the
   history source; `run-status.json` is a destroyed-per-iteration snapshot — PRD U16).
   Each iteration renders as the **4 labeled stages**, NOT a raw event dump (U23 —
   Temporal's thousands-of-events trap). Captured as the new canonical view
   `loop-flight-recorder` (already named in the frozen doc's BV11 "verified via").
3. **Virtualized run-log panel + drill-down (U38/U39):** bounded DOM over a large log
   (render only visible rows), tail by cursor, oversized individual records capped behind
   **lazy expand links** — never inlined, never a full-file DOM dump.

## Scope decisions (orchestrator's call — recorded, not silently assumed)

- **Transport stays polling.** Accepted PRD U7 fallback. SSE is NOT required for U2 — the
  flight recorder reads *history*, not a push stream. Agreed with the proposed scope.
- **U16 open question — RESOLVED (code-verified NO), Phase-1.** I code-verified the run-log
  producers in `cli/agentic_os.py` directly (not just the U1 STATE.md note):
  - `iteration` event (**line 1854**) carries `goal, iter, agg_iter, tokens, cum_tokens,
    changed, verdict, note` — **NO `criteria_passing`/`criteria_total`.**
  - `goal_end` event (**line 1696**) carries `goal, state, iterations, tokens, note,
    undo_pointer, session_id` — **also NO criteria counts** (only the terminal state).
  - `land_gate` event carries `goal, decision (land/flag/hold)` — no criteria counts.
  - Per-goal criteria counts live **only** in the current `run-status.json` snapshot
    (`goals[].criteria_passing/total`, written at `record_goal` line 1608), which is
    rewritten in place and destroys history.
  - **Decision:** the flight-recorder timeline reconstructs each iteration's **4 labeled
    stages + tokens + verdict + changed** from the run-log's existing per-iteration events
    (`iter_begin`/`iteration`/`land_gate`/`goal_end`). It does **NOT** claim a per-iteration
    criteria-over-time chart — that data is not in history. The **live** % ring's
    non-monotonic drop stays driven by the **UI's own observed series** across polls
    (unchanged from U1; `reader._observe`). **No producer/CLI extension in U2** — an engine
    change is out of the UI-slice lane (different subsystem; carries its own P0–P9 test debt,
    see Open failures) and is not required by any U2 criterion. Recorded here as a **deferred,
    non-U2 opportunity** should a future slice want a criteria-over-time chart.
- **Stack continuity.** stdlib-only server (`http.server`) + vanilla JS in `ui/assets`;
  virtualization needs no framework (windowing + line-clustering, GitHub's approach). No
  build toolchain, no new dependencies without a recorded justification.
- **OUT of scope:** U3 (skills-inventory surface, onboarding, glossary), U4 (control
  surface), C14 live ≥2-goal acceptance, SSE. **Fixtures-only** again — deterministic, no
  live `claude` needed.

## Anchors (checked at Phase-1 sign-off — all present in the TARGET)

- **Frozen design direction:** `docs/design/design-direction.md` (FROZEN 2026-07-16 v1 =
  C·Helm). §Motion rules are the load-bearing contract for U2. BV-list BV1–BV16 present.
- **References:** `docs/design/references/R3-helm-home-live-run.png` (primary anchor,
  present). R1/R2 pending file-drop (non-gating, per inherited context).
- **Baselines (regression anchor):** `docs/design/baselines/` — **13 promoted U1 views**
  present (`home-*` family). U2 must not regress them.
- **Contrast validator:** `docs/design/mocks/contrast-check.py` (exits 0 — token contract).

## Inherited architecture (don't rediscover)

- `ui/reader.py` — `StateReader`: torn-read-safe, read-only, secret-scrubbed derivation of
  the view model from `.agentic-os/` (`run-status.json`, `run-log.jsonl`, `queue.json`,
  `manifest.json`, `STATE.md`, `.claude/`). `_observe`/`_progress` drive the non-monotonic
  ring from the UI's OWN series. `_loop`/`_stage` derive the 4-stage graph + `here` marker.
- `ui/render.py` — SSR of the view model. `_render_live` builds the loop panel
  (`.lnode`/`.here`/`.livemark`) + ring + command deck + truth rail.
- `ui/assets/app.js` — polls `/api/state` ~1.5s, updates in place, ARIA live regions
  (empty-at-load), reduced-motion + theme toggles. **Never moves focus.**
- `ui/assets/app.css` + `tokens.css` — C·Helm layout; current motion is **near-zero**
  (`.lnode.live` static accent glow; the reduced-motion block hard-suppresses all animation
  globally). U2 is the first slice where reduced-motion actually has something to reduce.
- `ui/fixtures.py` — ONE builder for all canonical states, shared by tests + capture.
- `ui/capture_screens.py` — boots the real server per state + headless-Chrome capture; the
  independent verifier RE-RUNS it. Frozen capture cmd: `chrome --headless=new … --window-size
  1440,900 --screenshot`.
- `ui/server.py` — loopback-only (127.0.0.1) + Host-header allowlist; read-only.
- `tests/test_u1.py` — **self-contained** (own fixtures) → 39/39 standalone. U2's
  `tests/test_u2.py` must be self-contained too.

## Known pre-existing target issue (NOT U2's job)

`tests/test_p0..p9.py` need a never-committed `conftest.py` (the `base` fixture) → the engine
suite shows 38 errors on a fresh clone. This is recorded in the target's Open failures.
`test_u2.py` must be self-contained like `test_u1.py`; the engine suite's errors must not read
as a U2 regression. Do NOT edit or "fix" the engine tests as part of U2.

## Verification posture

- Vision-verify is MANDATORY (visual deliverable). The verifier RE-CAPTURES screenshots and
  judges by LOOKING (Read renders images) against the frozen direction + BV-list, and names
  the image files it viewed. Text-only verification of a UI slice is banned (B12).
- **Temporal claims** (motion budget=1, no fake-fill, ambient-motion) use the frozen
  **two-frame (before/after) procedure** across a state change — stills alone cannot verify
  motion (design-direction.md §capture; BV2/BV4/BV13).
- **No-regression:** the 13 promoted baselines must still match (re-capture + compare). Reuse
  U1's 3-lens adversarial accept shape (vision / regression+security / craft-skeptic).
- **Motion FEEL** stays in the **Human slot** — judged at the slice demo, not faked from a
  still (design-direction.md §Human slot).

## Sign-off

- **2026-07-16 — APPROVED as drafted.** User signed off on the 7-criterion rubric
  (C4/C8/C10/U2-LOOP/U2-FR/C15/C12) + BV1–BV16 verbatim + 6 process guards (BX1–BX6),
  max_iterations=5. `criteria.json` is LOCKED — criteria may only be ADDED with approval,
  never reworded/deleted (goal-opus rubric rule).
- **U16 scope call CONFIRMED by user: keep UI-only, no CLI/producer change.** The flight
  recorder reconstructs stages+tokens+verdict from the existing run-log; no criteria-over-time
  chart; the engine is untouched. Producer extension recorded as a deferred future-slice
  opportunity.
- `python tools/rubric_check.py` on the locked rubric: OK (valid rubric). Anti-pattern guard
  checked: no criterion's only route to `pass` triggers a banned outcome (each criterion is
  the inverse of the BV it maps to).

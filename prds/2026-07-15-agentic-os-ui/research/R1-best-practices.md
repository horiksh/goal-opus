# R1 — Newest Best Practices for the agentic-os UI/UX (2024–2026)

Research agent: **R1** (web-enabled, best-practices focus). Date: 2026-07-15.
Scope: cutting-edge, accessible, honest UI/UX for a **local-first, file-based, single-operator, Windows-first** dashboard over `.agentic-os/` files.

**Epistemic tags:** `[VERIFIED+SRC <url>]` = R1 read the primary source · `[REPORTED <url>]` = secondary source · `[ASSUMPTION]` = R1 inference, with a verification path. Every claim carries exactly one tag.

Working assumptions being researched against (from the product context): **A1** delivery = local web app (localhost server serves a browser dashboard); **A2** control = full control surface, phased read-only-first; **A3** scope = single-target/many-goals; **A4** success = daily-driver *and* visionary.

---

## Target 1 — Real-time / live-updating LOCAL dashboards (transport + torn-read safety)

**1.1 — SSE is the best-fit transport for a one-way, single-operator localhost dashboard.**
SSE is a one-way server→client channel ("This is a one-way connection, so you can't send events from a client to a server"), delivered as `text/event-stream` with events separated by a blank line. `[VERIFIED+SRC https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events]`
*Implication for PRD:* Default the live-update transport to SSE for the read-plane (run-status, log tail, progress); reserve request/response HTTP POST for control actions — no need for a bidirectional WebSocket.

**1.2 — SSE auto-reconnects natively; WebSocket does not.**
"By default, if the connection between the client and server closes, the connection is restarted," and the stream `id:` field sets the `EventSource`'s last-event-ID for resuming. WebSocket reconnection must be hand-written or libraried. `[VERIFIED+SRC https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events]`
*Implication for PRD:* Free resilience — if the local server restarts between goals, the browser silently reconnects; spec a `Last-Event-ID`/cursor on the run-log stream so the tail resumes without gaps.

**1.3 — Recommended escalation ladder: polling → SSE → WebSocket, only escalate when the model demands it.**
Guidance: "Start with polling for simple, infrequent updates. Graduate to SSE when you need efficient one-way real-time communication. Reserve WebSockets for truly interactive, bidirectional applications." `[REPORTED https://rxdb.info/articles/websockets-sse-polling-webrtc-webtransport.html]`
*Implication for PRD:* Since state changes at goal-iteration cadence (seconds+, not sub-second), even 1–2s polling is defensible for v1; SSE is the upgrade that removes poll latency. Do not adopt WebSocket — it adds bidirectional complexity this product does not need.

**1.4 — SSE's one real drawback (HTTP/1.1 6-connections-per-origin) is nearly irrelevant here, but pin the mitigation.**
"HTTP/1.1 browsers allow at most six simultaneous connections to the same origin"; an SSE stream holds one open permanently. "HTTP/2 multiplexes all streams over a single TCP connection… SSE's one practical constraint is the HTTP/1.1 connection limit, and HTTP/2 resolves it entirely." `[REPORTED https://textslashplain.com/2019/12/04/the-pitfalls-of-eventsource-over-http-1-1/]`
*Implication for PRD:* A single-operator dashboard uses ~1 SSE stream, so this rarely bites; still, spec **one** multiplexed event stream (not one per widget), or serve over HTTP/2, to stay safe if panels grow.

**1.5 — `run-status.json` is REWRITTEN per iteration, so the writer must write-temp-then-atomic-rename to prevent torn/partial reads.**
Atomic-write pattern: "first a temporary file containing the new content is written, then this file is renamed to the final path, this way it's impossible to get a corrupt/partially-written file"; `os.replace()` maps to atomic rename on POSIX/Windows same-volume. `[REPORTED https://github.com/fabiospampinato/atomically]` `[REPORTED https://lwn.net/Articles/974578/]`
*Implication for PRD:* Make atomic-replace a **hard requirement on the producer** (the goal-opus loop) and make the reader defensive: on JSON parse failure, keep the last-good snapshot and retry — never render a half-written state. Add a schema-version/`iteration` field so the UI can detect and debounce rapid rewrites.

---

## Target 2 — Agent / LLM-system OBSERVABILITY & CONTROL-PLANE UX

**2.1 — The canonical model is a nested trace: a run is a tree of typed observations (spans / events / generations).**
Langfuse records "the complete lifecycle of a request… Each trace captures every operation — LLM calls, retrieval steps, tool executions… along with timing, inputs, outputs" as "nested observations," grouped into sessions for multi-turn flows. `[VERIFIED+SRC https://langfuse.com/docs/tracing]`
*Implication for PRD:* Model the active run as a **tree of steps** (maker → verifier → land-gate → write-back), each with start/end time, inputs/outputs, and status — not a flat log; the run-log.jsonl events should carry parent/child ids so the UI can render the tree.

**2.2 — Leading tools visualize the run as an execution-flow / decision-path graph, not just text.**
"At DASH 2025, Datadog announced an execution flow chart that visualizes an agent's run and decision path, including inter-agent interactions, tool usage, and retrieval steps." LangSmith shows "the full execution tree… the internal monologue of the agent." `[REPORTED https://www.datadoghq.com/products/ai/agent-observability/]` `[REPORTED https://www.langchain.com/resources/agent-observability]`
*Implication for PRD:* Ship a run-timeline/flow view for the goal-opus lifecycle state machine (running/success/aborted/stopped/declined/flagged/held/no-progress) as first-class visual nodes, with the current node highlighted.

**2.3 — Observability's job is end-to-end visibility into every step of a long-running, self-directing agent — exactly the goal-opus loop.**
"Agent observability is end-to-end visibility into every step an AI agent takes… LLM calls, tool invocations, retrieval steps, and planning decisions," because single-LLM-call tooling "breaks when you deploy an agent that runs for ten minutes, calls fifteen tools, and decides its own control flow." `[REPORTED https://laminar.sh/article/2026-04-23-top-6-agent-observability-platforms]`
*Implication for PRD:* The dashboard is an observability plane first; every maker/verifier iteration must be inspectable after the fact (replay), not only live.

---

## Target 3 — TOKEN / COST visualization (budget-vs-spend, burn-down, forecast, attribution)

**3.1 — The proven dashboard primitives are: total spend, budget status, per-model/per-group breakdown, and a short-horizon projection.**
Open-source `llm-cost-dashboard` "renders a live dashboard showing total spend, per-model breakdowns, budget status, and projected monthly bills" with a rolling forecaster. Broadcom's dashboard shows "cumulative spend over time" plus input/output token split and a model-distribution chart. `[REPORTED https://github.com/Mattbusel/llm-cost-dashboard]` `[REPORTED https://techdocs.broadcom.com/us/en/ca-enterprise-software/it-operations-management/dx-operational-observability/saas/dashboards/all-dashboards/Out-of-the-Box-Dashboards/genai-and-llm-observability-dashboards/llm-cost-and-token-usage-dashboard.html]`
*Implication for PRD:* Token panel = (a) budget cap vs cumulative spend as a burn-down/gauge, (b) input/output token split, (c) **per-run/per-goal attribution** so "which goal ate the budget" is answerable at a glance.

**3.2 — Forecast-to-exhaustion must be labeled as an assumption, because it extrapolates current burn.**
"Projections assume current daily burn rate holds through end of month." `[REPORTED https://llmcosttracker.com/docs/dashboard]`
*Implication for PRD:* Any "tokens will run out in N iterations" figure must be visibly framed as a projection (dashed line / "at current rate") — never a hard promise; recompute per iteration from run-status.json.

**3.3 — Layered budget caps/quotas + threshold alerts are the norm for preventing overruns.**
Tools "enable limits and quotas at the level of keys, teams, or customers… set thresholds, receive alerts and enforce usage caps to keep AI costs within control before budgets are exceeded." `[REPORTED https://www.traceloop.com/blog/from-bills-to-budgets-how-to-track-llm-token-usage-and-cost-per-user]`
*Implication for PRD:* Surface the token cap as a first-class control; warn at (e.g.) 80% and visually mark the run that would breach the cap — ties into the loop's own bounded-budget stop condition.

---

## Target 4 — PROGRESS / percent-complete when "percent" = criteria-passing (honest progress)

**4.1 — Determinate over indeterminate whenever a real number exists.**
"For the sake of transparency, use determinate indicators in every possible instance that you can." `[REPORTED https://usersnap.com/blog/progress-indicators/]`
*Implication for PRD:* `criteria_passing / criteria_total` is a real, honest determinate fraction — show it as a determinate bar/ring, not a spinner. This is a genuine strength of the Default-FAIL rubric.

**4.2 — Percent-done indicators create speed expectations; changes in pace erode trust — so pace progress honestly.**
NN/g: "A percent-done indicator makes users develop an expectation for how fast the action is being processed… changes in speed will be noticed and will impact user satisfaction," and advise a general (not exact) estimate. `[VERIFIED+SRC https://www.nngroup.com/articles/progress-indicators/]`
*Implication for PRD:* Because criteria flip discretely (and can regress), the bar can jump or move backward. Design for **non-monotonic progress**: show criteria as discrete pips/checklist (N of M passing) rather than implying smooth linear advance, and never animate fake in-between motion.

**4.3 — Don't fake a percentage you don't have; a wrong estimate is its own trust problem.**
"You can't show an accurate percentage because you don't have one, and some say you should fake a percentage anyway, but that creates a different kind of trust problem when the estimate turns out to be wildly off." `[REPORTED https://usersnap.com/blog/progress-indicators/]`
*Implication for PRD:* When no criterion has flipped yet (Default-FAIL start = 0/M), show an honest "0 of M criteria met — not started" empty/zero state, not a comforting animation implying progress.

**4.4 — Determinate = system can measure completion; indeterminate = it cannot.**
Determinate indicators are used "when the system can accurately estimate how much of it has been completed"; indeterminate ones "when the system cannot predict the task duration or measure progress." `[REPORTED https://mobbin.com/glossary/progress-indicator]`
*Implication for PRD:* Split the two truthfully: **goal completion** = determinate (criteria fraction); the **live "maker is thinking"** micro-state within an iteration = indeterminate (spinner/pulse), clearly a different, smaller indicator.

---

## Target 5 — Accessibility for live dashboards (WCAG 2.2, color-independence, motion, live regions)

**5.1 — WCAG 2.2 SC 1.4.1 Use of Color (Level A): color must never be the only carrier of meaning.**
"Color is not used as the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element." Intent: color-deficient, low-vision, older, and monochrome-display users can't rely on color alone. `[VERIFIED+SRC https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html]`
*Implication for PRD:* Every run/state color (running/success/aborted/stopped/declined/flagged/held/no-progress) MUST pair with an icon or text label — this is a hard, testable acceptance criterion, not a nicety.

**5.2 — Pair status color with a distinct icon/shape + text; simulate colorblindness to verify.**
Use "universally recognizable icons or symbols (checkmark for success, X for error, exclamation for warning) in conjunction with color," add text labels, and "use browser extensions or online tools to simulate… protanopia, deuteranopia, tritanopia." `[REPORTED https://www.thewcag.com/criteria/1.4.1]`
*Implication for PRD:* Define a status token set = {color + glyph + label} as one atomic component; add a colorblind-simulation check to the visual-verify step (this repo mandates vision-verify for visual work).

**5.3 — WCAG 2.2 SC 4.1.3 Status Messages (Level AA): live updates must be announced without moving focus.**
"Status messages can be programmatically determined through role or properties such that they can be presented… by assistive technologies without receiving focus" — via `role="status"`/`role="alert"` and `aria-live`. `[VERIFIED+SRC https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html]`
*Implication for PRD:* The live regions (run-status changes, "iteration N complete", token-threshold warnings) need ARIA live regions; a per-iteration rewrite must not steal focus.

**5.4 — Use `aria-live="polite"` for routine updates, reserve `assertive`; give updates context.**
"Avoid making all updates assertive… causing frustration"; include a context label like "New message received" not just "Received." `polite` announces when the user is idle. `[REPORTED https://www.uxpin.com/studio/blog/aria-live-regions-for-dynamic-content/]`
*Implication for PRD:* Routine iteration/progress updates → `polite`; only budget-exhaustion / run-aborted → `assertive` (`role="alert"`). Announce meaning ("Goal X: 4 of 6 criteria now passing"), not raw diffs.

**5.5 — `prefers-reduced-motion: reduce` signals an OS-level request to remove/replace non-essential motion.**
The `reduce` value "indicates that a user has enabled the setting on their device for reduced motion… the browser… removes, reduces, or replaces motion-based animations" (can trigger vestibular discomfort). `[VERIFIED+SRC https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion]`
*Implication for PRD:* Honor `prefers-reduced-motion` at the CSS layer; also offer an in-app toggle (localStorage OR media query) for shared/undiscovered-setting cases.

---

## Target 6 — Empty / loading / error / offline / first-run states

**6.1 — These "in-between" states are where AI-built dashboards fail most, and where trust is won or lost.**
A cited 2025 NN/g analysis of 50 AI-generated dashboards: "92 percent had no empty state design, 78 percent had no error state design, and 100 percent had a generic spinner"; human-designed dashboards handled all three ~70% of the time. `[REPORTED https://blog.vibecoder.me/empty-states-loading-states-error-states]`
*Implication for PRD:* Treat empty/loading/error/offline/first-run as **required deliverables with their own acceptance criteria**, not afterthoughts — first-run (no goals yet, no `.agentic-os/` populated) especially.

**6.2 — Model UI state as an explicit finite set to keep behavior predictable.**
"Define a simple union: `type RequestState = 'idle' | 'loading' | 'error' | 'success'`." `[REPORTED https://blog.logrocket.com/ui-design-best-practices-loading-error-empty-state-react/]`
*Implication for PRD:* Each panel (skills, tokens, queue, active-run, progress) declares an explicit state enum incl. `no-data`, `stale`, `parse-error`; the UI renders per-panel, so one missing file doesn't blank the whole dashboard.

**6.3 — Offline/error copy should state the problem plainly and what the user can still do.**
"State the problem directly ('You are currently offline')" and "explain what the user can still do." `[REPORTED https://blog.logrocket.com/ui-design-best-practices-loading-error-empty-state-react/]`
*Implication for PRD:* If the local server/loop is not running, show "Loop not running — showing last snapshot from <time>" with the last-good data, not a dead spinner. Distinguish "loop stopped" from "dashboard disconnected."

---

## Target 7 — Performance for live dashboards (long append-only log, virtualization)

**7.1 — Virtualize the run-log: render only visible rows to hold 60fps over thousands of lines.**
"By rendering only visible content, 60 FPS performance can be achieved even with tens of thousands of items"; virtualization keeps the DOM at a fixed ~20–30 nodes and recycles them. Log viewers are a named use case. `[REPORTED https://ehosseini.info/articles/list-virtualization/]`
*Implication for PRD:* `run-log.jsonl` grows unbounded (append-only) — the log/timeline panel MUST use list virtualization (e.g. TanStack Virtual) from day one, not render every line.

**7.2 — TanStack Virtual is the current framework-agnostic default with dynamic row heights.**
"As of November 2024, TanStack Virtual is the most popular library… framework-agnostic, highly performant… vertical, horizontal, and grid layouts, dynamic row heights, and a 60 FPS performance guarantee." `[REPORTED https://tanstack.com/virtual/v3]`
*Implication for PRD:* Name a concrete virtualization approach in the tech section; dynamic row heights matter because log events vary in length (multi-line errors vs one-line events).

**7.3 — Append-only + tail: read incrementally, don't re-parse the whole file each tick.**
Atomic/crash-safe JSONL patterns favor append + offset tracking over full rewrites for event streams. `[REPORTED https://dev.to/constanta/crash-safe-json-at-scale-atomic-writes-recovery-without-a-db-3aic]`
*Implication for PRD:* The server should tail `run-log.jsonl` from a byte offset and push only new events over SSE; the browser appends to a virtualized list — never resend the full log.

---

## Target 8 — Motion / animation for a "visionary" feel without harming legibility

**8.1 — Functional UI motion is short: ~150–200ms desktop, 100–200ms for quick actions.**
"Desktop animations should last 150ms to 200ms… for quick, straightforward actions like button clicks, shorter animations in the range of 100–200ms are usually ideal," with asymmetric ease-out preferred. `[REPORTED https://m1.material.io/motion/duration-easing.html]`
*Implication for PRD:* Budget transitions at ~150–250ms with ease-out; motion should signal state change (a criterion flipping, a run entering a new state), not decorate.

**8.2 — When you disable motion, replace (don't just delete) motion that conveyed state.**
"A static alternative to the animation is needed if disabling an animation would hide information, stop a process indicator, or make content unclear"; "replace them with opacity fades or color shifts so the interface still feels responsive." `[REPORTED https://blog.pope.tech/2025/12/08/design-accessible-animation-and-movement/]`
*Implication for PRD:* Every meaningful animation needs a reduced-motion fallback that still communicates the change (e.g., criterion flip = instant color+icon swap instead of a sweep). WCAG 2.3.3 (Animation from Interactions, AAA) is the reference. `[REPORTED https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html]`

**8.3 — Motion must respond to input and feel purposeful ("meaningful motion"), a lever for the visionary target.**
Material motion "responds to the user's input without missing a beat" and draws on physical forces (gravity/friction) to feel natural. `[REPORTED https://m1.material.io/motion/material-motion.html]`
*Implication for PRD:* The "visionary" A4 goal is met through *meaningful* motion (progress rings filling as criteria pass, run-state morph transitions), not gratuitous effects that fight legibility on a dense data plane.

---

## Target 9 — Security for a localhost server exposing local repo files

**9.1 — Binding to 127.0.0.1 is necessary but NOT sufficient; DNS rebinding can reach loopback services from a malicious web page.**
Browsers "don't update their same-origin policy when a DNS lookup resolves to a different IP"; an attacker serves from a public IP then rebinds to loopback, and "the browser treats requests as coming from the same origin." (Real precedent: Ollama CVE-2024-28224.) `[VERIFIED+SRC https://github.blog/security/application-security/dns-rebinding-attacks-explained-the-lookup-is-coming-from-inside-the-house/]` `[REPORTED https://unit42.paloaltonetworks.com/dns-rebinding/]`
*Implication for PRD:* Loopback bind (`127.0.0.1`, never `0.0.0.0`) is table stakes; the threat model MUST also list DNS rebinding. This directly affects a tool that serves local repo files.

**9.2 — Primary DNS-rebinding defenses for a localhost app: Host-header allowlist + strong auth even over HTTP.**
"Check the Host header of the request and deny if it doesn't strictly match an allow list"; "use strong authentication, even if it is over unencrypted HTTP" (rebinding requests don't carry the app's cookies). `[VERIFIED+SRC https://github.blog/security/application-security/dns-rebinding-attacks-explained-the-lookup-is-coming-from-inside-the-house/]`
*Implication for PRD:* Requirements: (a) reject requests whose `Host` isn't `localhost`/`127.0.0.1[:port]`; (b) a per-session local token/secret for control actions even though it's localhost; (c) precedent — the MCP ecosystem shipped the same fix (rmcp streamable-HTTP DNS-rebinding advisory GHSA-89vp-x53w-74fx). `[REPORTED https://github.com/modelcontextprotocol/rust-sdk/security/advisories/GHSA-89vp-x53w-74fx]`

**9.3 — For control actions, default session cookies to `SameSite=Lax` (or use CSRF tokens) to blunt CSRF.**
"Start with SameSite=Lax as your default… excellent CSRF protection while maintaining good UX"; if the framework lacks built-in CSRF protection, "add CSRF tokens to all state-changing requests and validate them." `[REPORTED https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html]`
*Implication for PRD:* Phase-2 control surface (enqueue/run/pause/steer/undo/approve) = state-changing POSTs → require CSRF token + SameSite=Lax; read-only phase-1 (GET/SSE) is lower-risk but still needs the Host allowlist.

**9.4 — Don't re-leak secrets the pipeline already scrubbed.**
(No single canonical URL; general secure-logging practice.) `[ASSUMPTION]` — verify by auditing what run-status.json / run-log.jsonl / STATE.md actually contain before the UI renders them; if the loop scrubs API keys/tokens from logs, the UI must not surface a rawer source that reintroduces them.
*Implication for PRD:* The UI reads only the already-scrubbed local files and adds no new exfiltration path (no sending file contents to any remote endpoint); add a "never renders raw secrets" acceptance check.

---

## Target 10 — Design-system / dark-mode / information-density norms for dev tools (2024–2026)

**10.1 — Dark-first is the modern default for developer tools, not a toggle.**
"Products like Linear and Vercel treat dark as the default, not a toggle"; "Arc Browser, Linear, Warp, and Raycast all launched dark-first. Their light modes… feel secondary." `[REPORTED https://www.aydesign.ai/blog/dark-mode-dashboard-patterns-2026]`
*Implication for PRD:* Design the dashboard dark-first (this is a solo-dev tool used in a dark editor context), with light mode as a supported second theme — both must pass contrast + color-independence.

**10.2 — Dark surfaces = true grey (not pure black), layered elevation via lightness, single saturated accent.**
The dominant dark patterns: "true grey base surfaces (not pure black), layered elevation through background lightness, single saturated accent in a desaturated system, borderless cards with elevation tokens… dark-first data-visualization palettes." `[REPORTED https://muz.li/blog/dark-mode-design-systems-a-complete-guide-to-patterns-tokens-and-hierarchy/]`
*Implication for PRD:* Define tokens: grey base (not #000), elevation-by-lightness layers, one accent color, and a **separate status palette** (from 5.1/5.2) that is colorblind-safe against the dark base.

**10.3 — For daily-driver calm, prefer restraint: ~5–9 core elements, not a dense wall of charts.**
"The most effective SaaS dashboards display between five and nine core elements"; "whitespace and calm design outperform data-dense layouts for daily-use tools." A persistent sidebar is the standard nav for multi-section tools. `[REPORTED https://www.925studios.co/blog/saas-dashboard-design-examples-2026]`
*Implication for PRD:* Resist cramming — the four mandated mechanics (skills, tokens, running goals, %-to-goal) map to ~4 primary panels + a sidebar; depth (full trace/log) lives one click down, not all on the top surface. Balances A4 (daily-driver AND visionary).

**10.4 — Fine-grained gray scale gives every border/divider/disabled state a deliberate step.**
Vercel's language: near-white `#fafafa` body, ink `#171717` type, "a 200-step gray scale where every divider, border, and disabled state lives on its own deliberate step." `[REPORTED https://www.shadcn.io/design/vercel]`
*Implication for PRD:* Adopt a multi-step neutral ramp as design tokens so density reads as intentional hierarchy rather than noise — critical when the log/trace plane is information-dense.

---

## Cross-cutting synthesis (for the PRD authors)

- **Transport:** SSE (single multiplexed stream, auto-reconnect, `Last-Event-ID` cursor) for the read-plane; HTTP POST + CSRF token for the phase-2 control-plane. Polling is an acceptable v1 fallback given iteration-cadence updates. `[VERIFIED+SRC MDN SSE]` + `[REPORTED rxdb]`
- **Data integrity:** producer writes `run-status.json` via temp-file + atomic rename; reader keeps last-good snapshot on parse failure; log is tailed by offset over SSE, never re-sent whole. `[REPORTED atomically/LWN]`
- **Honesty:** determinate progress = criteria fraction shown as discrete pips (supports regression); no faked motion; forecasts labeled "at current rate." `[VERIFIED+SRC NN/g]`
- **Accessibility is acceptance-testable:** 1.4.1 color-independence (color+icon+label), 4.1.3 live regions (polite default, assertive for aborts), prefers-reduced-motion with replacement fallbacks. `[VERIFIED+SRC W3C x2 + MDN]`
- **Security is threat-modeled:** loopback bind + Host allowlist + local auth token (DNS-rebinding), never render already-scrubbed secrets. `[VERIFIED+SRC GitHub blog]`
- **Look:** dark-first, true-grey elevation, single accent, colorblind-safe status palette, ~5–9 calm top-level elements with depth one click down. `[REPORTED muz.li / 925studios / shadcn]`

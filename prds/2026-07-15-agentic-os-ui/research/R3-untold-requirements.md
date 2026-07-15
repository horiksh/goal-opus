# R3 — Untold-Requirements Mining: agentic-os UI/UX

**Focus:** requirements the user did NOT state but the domain + its evidence demand. Every item is a testable
"the UI MUST …" with an evidence trace and an epistemic tag:
`[VERIFIED+SRC <url>]` (primary source read) · `[REPORTED <url>]` (secondary source) · `[ASSUMPTION]` (with verification path).
"Untold ≠ invented": each traces to an analog failure mode, a standard, or a demonstrable norm.

Product reality this UI sits on: a LOCAL-FIRST, FILE-BASED, single-operator, Windows-first CLI runs a bounded
self-improving loop and **writes** `.agentic-os/run-status.json` (rewritten in place per iteration),
`.agentic-os/run-log.jsonl` (append-only), `.agentic-os/queue.json`, `STATE.md`, and git checkpoints. The UI is a
localhost web app that **reads those files concurrently while the CLI writes them.** That reader/writer split is the
source of most untold requirements below.

---

## 1. Concurrency / Data Integrity

**R1.1 — The UI MUST treat every `run-status.json` read as possibly torn (mid-rewrite): on JSON parse failure it MUST
retry after a short delay and fall back to the last-known-good value, and MUST NOT render a parse failure as "no run"
or a blank dashboard.**
Evidence: a file rewritten in place can be caught mid-write; readers that don't retry surface "logically invalid"
content. Torn writes "leave the system in an inconsistent state where the file structure remains intact but the content
is logically invalid." `[REPORTED https://dev.to/constanta/crash-safe-json-at-scale-atomic-writes-recovery-without-a-db-3aic]`

**R1.2 — The PRD MUST specify that the CLI writer uses write-temp-then-atomic-rename (temp file in the SAME directory,
fsync, atomic replace) for `run-status.json`, and the UI MUST be designed assuming that contract — and detect/annotate
its absence rather than assuming clean reads.**
Evidence: the canonical safe-write pattern is "write to a temp file next to the target, flush() and fsync(), then
atomically swap with os.replace()"; both paths must be on the same filesystem or you silently get non-atomic
copy+delete. `[REPORTED https://python-atomicwrites.readthedocs.io/]` `[REPORTED https://github.com/npm/write-file-atomic]`

**R1.3 — (Windows-first, load-bearing) The UI reader MUST tolerate a transient "file missing"/sharing-violation on
`run-status.json` during the writer's rename, retrying a few times before ever declaring the file absent.**
Evidence: POSIX guarantees a concurrent reader never sees the destination missing during rename; Windows does NOT give
that guarantee — `MoveFileEx` "is usually atomic, but in some cases it will silently fall-back to a non-atomic method,"
and the safe approach is `ReplaceFile`/`os.Replace`. On a Windows target the reader can momentarily hit ENOENT or a
sharing violation mid-swap. `[REPORTED https://github.com/golang/go/issues/8914]`
`[REPORTED https://learn.microsoft.com/en-us/archive/msdn-technet-forums/449bb49d-8acc-48dc-a46f-0760ceddbfc3]`

**R1.4 — The UI MUST parse `run-log.jsonl` line by line, keeping any incomplete trailing line buffered for the next
read, and MUST skip/log a single malformed record rather than failing the whole file.**
Evidence: "If a writer crashes mid-record, the final line is incomplete. A reader should parse lines independently and
skip or log the broken final line rather than failing the whole file." The standard tail pattern buffers chunks, splits
on `\n`, and holds the incomplete last line. `[REPORTED https://jsonlines.org/]` `[REPORTED https://jsonparser.com/ndjson-guide]`

**R1.5 — The UI MUST be strictly read-only on every CLI-owned file in v1 (never open for write, lock, or truncate
them); any UI-owned state (view prefs, action audit) MUST live in separate, UI-owned files.**
Evidence: single-writer discipline is what makes the atomic-rename contract hold; a second writer/locker can corrupt or
block the file the CLI owns. `[ASSUMPTION — verify against the CLI's file-ownership/locking model in docs/context and the run-status writer]`

---

## 2. Stale / Crash State

**R2.1 — The UI MUST detect a crashed run: `in_flight:{goal,iter}` present on disk with no matching `session_end` is a
crash marker, and the UI MUST render an explicit "crashed mid-iteration" state — never "running".**
Evidence: product context states `in_flight` with no `session_end` means the last run crashed mid-iteration; a naive UI
would keep showing the last "running" frame forever. `[ASSUMPTION — verify exact fields/semantics against run-status.json schema]`

**R2.2 — The UI MUST compute liveness from freshness (file mtime / heartbeat staleness threshold), NOT from the presence
of a "running" status string, and MUST flip to a "stale — possibly dead" state once the threshold is exceeded.**
Evidence: transports and writers stop without emitting a terminal event; freshness is the only reliable liveness signal.
SSE guidance treats reconnection/last-event tracking as the mechanism precisely because a "running" flag can't be
trusted after a drop. `[REPORTED https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events]`

**R2.3 — The UI MUST visually distinguish "CLI alive but idle/between iterations" from "CLI process dead," and MUST NOT
present frozen last-known data as if it were live.**
Evidence: same freshness principle; showing frozen data as live is the core live-update failure mode (see R4.2). `[ASSUMPTION — verify whether the CLI emits an idle/heartbeat signal or only per-iteration rewrites]`

---

## 3. Empty / First-run / Not-installed States

**R3.1 — The UI MUST render a coherent "not initialized" state when `.agentic-os/` does not exist on the target
(guidance on how to init), not an error stack, blank screen, or spinner-forever.**
Evidence: first-run/empty-state is a baseline usability norm; the product context flags "target not initialized (no
`.agentic-os/`)" as a required state. `[ASSUMPTION — norm; verify by pointing the UI at a fresh repo]`

**R3.2 — The UI MUST handle "no run has ever happened," "no goals queued," and "goals queued but none run" as three
distinct empty states, each with an appropriate affordance, not one generic "nothing here."**
Evidence: product context enumerates these as separate first-run conditions; conflating them hides actionable state.
`[ASSUMPTION — verify against queue.json + run-log.jsonl absence combinations]`

**R3.3 — The UI MUST not crash or error-toast on missing or zero-length `run-log.jsonl` / `run-status.json` / `queue.json`
(files may not exist yet before the first run).**
Evidence: append-only logs start empty; readers must treat empty/missing as a valid state. `[REPORTED https://blog.liquid-technologies.com/json-lines-large-log-files]`

---

## 4. Live-Update Reliability

**R4.1 — If the UI streams updates (SSE/WebSocket), it MUST auto-reconnect with backoff on transport drop and resume
without gaps or duplicates (SSE `id`/`Last-Event-ID`, or a since-cursor for the log tail).**
Evidence: EventSource "automatically reconnects" with a `retry` delay, and `Last-Event-ID` lets the server "resume
transmission from the correct position," preventing dupes/gaps on reconnect. `[REPORTED https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events]`
`[REPORTED https://http.dev/last-event-id]`

**R4.2 — The UI MUST display "last updated Ns ago" and visibly switch to a stale indicator when updates stop, so frozen
data is never silently shown as live.**
Evidence: freshness/staleness surfacing is the standard mitigation for the "is this live or dead?" failure; ties to R2.2.
`[REPORTED https://singhajit.com/server-sent-events-explained/]`

**R4.3 — Polling implementations MUST bound their rate and back off on repeated read/parse failure (not hammer a file
being rewritten), and MUST not pin CPU on a long-running dashboard.**
Evidence: retry-on-parse-fail (R1.1) without backoff degrades into a busy-loop against the writer. `[REPORTED https://dev.to/constanta/crash-safe-json-at-scale-atomic-writes-recovery-without-a-db-3aic]`

---

## 5. Security / Privacy of a Localhost Server Exposing Repo Files

**R5.1 — The server MUST bind to the loopback interface (127.0.0.1) only, never 0.0.0.0.**
Evidence: "Binding a service to 127.0.0.1 inherently restricts access to the local machine … external entities cannot
access services bound to the loopback address"; 0.0.0.0 "exposes the service to all network interfaces, which might
include public networks." `[REPORTED https://thelinuxcode.com/127001-vs-0000-what-they-mean-when-to-use-each-and-how-to-debug-binding-bugs/]`

**R5.2 — The server MUST defend against DNS rebinding by validating the `Host` header against an allowlist
(`localhost`/`127.0.0.1[:port]`) and rejecting mismatches; loopback binding alone is NOT sufficient.**
Evidence: DNS rebinding lets a malicious public web page reach services "bound to 127.0.0.1 without VPN or port
forwarding"; the documented mitigation is "Check the Host header of the request and deny if it doesn't match expected
values." A real MCP-on-localhost CVE (CVE-2025-66414) demonstrates the class. `[REPORTED https://github.blog/security/application-security/dns-rebinding-attacks-explained-the-lookup-is-coming-from-inside-the-house/]`
`[REPORTED https://en.wikipedia.org/wiki/DNS_rebinding]`

**R5.3 — Any state-changing endpoint MUST carry CSRF protection (per-session token + Origin/Referer check, SameSite
cookies), because a localhost web UI is reachable cross-site from any page the operator visits.**
Evidence: DNS-rebinding + CSRF against localhost dev tools is the documented attack surface; the rebinding writeups
frame localhost as "not as private as you think." `[REPORTED https://iamanuragh.in/blog/2026-04-12-dns-rebinding-your-localhost-is-not-as-private-as-you-think/]`

**R5.4 — The UI MUST NOT re-leak secrets even though the CLI has a pre-write scrub (defense in depth): treat
`STATE.md` / `run-log` / `run-status` content as potentially secret-bearing, and MUST NOT echo raw content into URLs/
query strings, page titles, notifications, or exports.**
Evidence: product context states the scrub exists but the rubric/guardrails are "gameable" and NOT a security guarantee;
a single upstream scrub is not a reason for the display layer to trust the data. Privacy rule: never place sensitive
data in URL parameters. `[ASSUMPTION — verify scrub coverage; treat as best-effort, layer a display-time redaction]`

**R5.5 — If the server serves any file by path, it MUST canonicalize and confine paths to the target repo root and
reject traversal (`..`, absolute paths, symlink escape).**
Evidence: path traversal is the standard failure for a server that maps requests to files; the product context flags it
explicitly. `[ASSUMPTION — standard control; verify against the server's file-serving routes]`

---

## 6. Write-Path Safety (phased control surface: enqueue/run/pause/steer/undo/approve)

**R6.1 — Destructive/irreversible actions (undo = git reset to a pre-change SHA; stop/pause) MUST require an explicit
confirmation that names exactly what will happen (target SHA, goal, iteration) before executing.**
Evidence: product context defines `undo` as a git reset; irreversible controls require confirmation (matches this
agent's own action-safety norms for irreversible operations). `[ASSUMPTION — verify undo semantics against the CLI's git-checkpoint model]`

**R6.2 — The UI and CLI MUST NOT both drive the loop at once: UI-initiated mutations MUST use optimistic concurrency —
carry a precondition (expected current iter/SHA or a lease) and be rejected if on-disk state has moved.**
Evidence: two concurrent drivers of a single-threaded loop is a classic lost-update/split-brain hazard; the file
substrate has no built-in locking. `[ASSUMPTION — verify whether the CLI exposes a lock/lease or a compare-and-set entry point]`

**R6.3 — UI-initiated actions MUST be idempotent / de-duplicated (client-generated action id) so a retry after a dropped
response cannot double-apply (e.g., double-undo, double-enqueue).**
Evidence: on an auto-reconnecting transport (R4.1) a response can be lost while the action succeeded; idempotency is the
standard guard. `[REPORTED https://http.dev/last-event-id]`

**R6.4 — Every UI-initiated action MUST be recorded to a UI-owned audit trail (who/when/what/result), separate from the
CLI's run-log, so autonomous vs operator-initiated changes remain distinguishable.**
Evidence: the system's stated design value is that autonomous changes stay "bounded, VISIBLE, and REVERSIBLE"; operator
actions through a new surface must inherit the same visibility. `[ASSUMPTION — derived from the stated observability invariant]`

---

## 7. Accessibility

**R7.1 — Run/goal/criterion state MUST be conveyed by more than color (icon, text label, or shape in addition to hue).**
Evidence: WCAG 2.1 SC 1.4.1 (Level A): "color is not used as the only visual means of conveying information … or
distinguishing a visual element"; ~1 in 12 men have color-vision deficiency. `[VERIFIED+SRC https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html]`

**R7.2 — Live-updating status and metrics (tokens used/available, % to goal, run state) MUST be exposed to assistive
tech via `aria-live`/`role=status` so screen readers announce changes without the element receiving focus.**
Evidence: WCAG 2.1 SC 4.1.3 Status Messages (Level AA): status messages "can be programmatically determined through
role or properties such that they can be presented to the user by assistive technologies without receiving focus,"
implemented via `role=status`/live regions. `[VERIFIED+SRC https://www.w3.org/WAI/WCAG21/Understanding/status-messages.html]`

**R7.3 — All "visionary" motion (animated meters, flowing token counters, transitions) MUST honor
`prefers-reduced-motion` and drop to a static/dampened presentation when the OS setting is on.**
Evidence: W3C technique C39 uses the `prefers-reduced-motion` media query to "prevent motion"; motion can cause
"dizziness, nausea, headaches" for users with vestibular disorders (WCAG 2.3.3). `[VERIFIED+SRC https://www.w3.org/WAI/WCAG22/Techniques/css/C39]`

**R7.4 — The dashboard MUST be fully keyboard operable: every control (enqueue/run/pause/undo/approve, log navigation)
reachable and actuatable without a pointer.**
Evidence: keyboard operability is WCAG 2.1.1 (Level A), baseline for any interactive UI. `[REPORTED https://webaim.org/techniques/aria/]`

**R7.5 — Live regions MUST be present in the DOM at page load (empty), and routine metric updates MUST use
`aria-live="polite"` (not `assertive`), reserving `assertive`/`role=alert` for crash/block/budget alerts only.**
Evidence: "declare the live region in the DOM before you put content in it … if you inject the container and content at
the same time, many screen readers miss the announcement"; assertive "will interrupt … can be extremely annoying …
use sparingly." `[REPORTED https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live]`

---

## 8. Progress Honesty ("% to goal")

**R8.1 — "% to goal" MUST be defined and labeled as `criteria_passing / criteria_total` (against the locked rubric),
not presented as time, effort, or ETA.**
Evidence: product context defines progress as criteria-passing ratio; "most progress indicators are vastly
misinterpreted by non-technical users as accurate feedback" when their basis is unstated. `[REPORTED https://blog.jim-nielsen.com/2023/faux-progress/]`

**R8.2 — The progress display MUST be non-monotonic-safe: a criterion can regress from passing to failing, so the bar
MUST be able to go DOWN, and the UI MUST NOT lock a "high-water mark" or auto-advance toward 100%.**
Evidence: product context states % to goal is non-monotonic; "misleading progress indicators that fill up without
showing real progress hurt user trust quickly." `[REPORTED https://bricxlabs.com/blogs/progress-bar-ux-examples]`

**R8.3 — The UI MUST NOT apply "benevolent deception" (easing/fake-fill animations that imply progress not grounded in
criteria state). This is an observability tool, not a consumer wait screen — honesty overrides comfort.**
Evidence: consumer UIs use "benevolent deception … visual tricks to make bars feel faster"; that pattern is a deceptive
pattern when the number is supposed to be a truthful system readout. `[REPORTED https://blog.jim-nielsen.com/2023/faux-progress/]`
`[REPORTED https://www.linkedin.com/posts/nielsen-norman-group_deceptive-patterns-in-ux-how-to-recognize-activity-7137467820254138370-zyaB]`

**R8.4 — "Done" / 100% MUST reflect an actual land-gate pass (verifier-confirmed), never be shown optimistically while
an iteration is still in flight or before write-back completes.**
Evidence: the loop only "lands" after independent verification + write-back; a premature 100% is a fake-completion
deceptive pattern. `[ASSUMPTION — verify terminal-state semantics in run-status.json / land-gate]`

---

## 9. Observability of the UI Itself + Data Lifecycle

**R9.1 — The UI MUST offer export/share of a run (snapshot: run-status + a bounded log slice + criteria), and MUST
re-apply secret redaction at export time (do not assume the on-disk file is already clean — see R5.4).**
Evidence: product context lists "export/share a run" as a data-lifecycle need; combined with the "scrub is gameable"
warning, export is a fresh leak surface. `[ASSUMPTION — pair with R5.4 verification]`

**R9.2 — The UI MUST handle a large `run-log.jsonl` (thousands of lines) without freezing: stream/tail/paginate, cap
in-memory rows, and define an explicit performance ceiling.**
Evidence: JSONL is chosen for large logs precisely so you "add new records without re-parsing or re-writing the entire
file"; a UI that loads the whole file into memory defeats that and stalls on long runs. `[REPORTED https://blog.liquid-technologies.com/json-lines-large-log-files]`

**R9.3 — The PRD MUST address `run-log.jsonl` rotation/retention (unbounded growth over a long run), and the UI MUST
behave correctly across a rotation (file replaced/truncated) — resetting its tail cursor rather than reading garbage.**
Evidence: append-only logs grow unbounded; the tail reader holds a byte/line cursor that a rotation invalidates. `[REPORTED https://ndjson.com/advantages/]`

**R9.4 — The UI MUST surface its OWN error surface (cannot read file, elevated parse-failure rate, server/transport
disconnected) as visible in-UI state, not fail silently or only in the browser console.**
Evidence: a monitoring UI that hides its own read failures becomes a source of false confidence — the "frozen shown as
live" failure (R4.2) generalized to all UI internals. `[REPORTED https://singhajit.com/server-sent-events-explained/]`

---

## 10. Anything Else the Evidence Demands

**R10.1 — The UI MUST show timestamps as relative + absolute with explicit timezone, and MUST tolerate clock skew when
computing mtime-based staleness (a backward clock jump must not read as "fresh forever" or "infinitely stale").**
Evidence: mtime/heartbeat staleness (R2.2) is only as reliable as the clock; local-first single-machine apps still hit
sleep/resume and manual clock changes. `[ASSUMPTION — verify staleness computed from monotonic delta where possible]`

**R10.2 — The UI MUST be forward-compatible with the on-disk schema (ignore unknown fields, default missing ones,
degrade gracefully on version bump) because the CLI evolves independently of the UI.**
Evidence: reader and writer ship separately; strict schema coupling would break the dashboard on any CLI update. `[ASSUMPTION — verify whether run-status.json carries a schema/version field]`

**R10.3 — The UI MUST accurately reflect `queue.json` goal states (pending vs `consumed`) and handle a goal flipping to
`consumed` while displayed (concurrent consumption by the CLI) without showing a stale "pending" as runnable.**
Evidence: product context notes goals get `consumed` flags written by the CLI while the UI reads the same file — the
same reader/writer race as R1.1 applied to the queue. `[ASSUMPTION — verify queue.json consumed-flag semantics]`

**R10.4 — In-browser notifications MUST reconcile with the existing push-notify hook (AGENTIC_OS_NOTIFY_CMD) events
(finish/block/budget/decline) — one source of truth, no duplicate or contradictory alerts between the two channels.**
Evidence: product context states a push-notify hook already fires on those transitions; a second notification surface
must not double-fire or diverge. `[ASSUMPTION — verify the notify hook's event set and delivery guarantees]`

---

### Verification backlog (ASSUMPTION items to close before/with the PRD)
- run-status.json exact schema: `in_flight`, `session_end`, terminal states, version field (R2.1, R8.4, R10.2).
- CLI writer's actual write strategy (temp+rename? fsync? Windows ReplaceFile?) (R1.2, R1.3).
- Whether the CLI exposes any lock/lease/CAS entry point for a control surface (R6.2).
- Scrub coverage vs. what still reaches STATE.md/run-log on disk (R5.4, R9.1).
- queue.json consumed-flag write semantics (R10.3) and notify-hook event set (R10.4).

# R4 — Adversarial Gap-Check of the agentic-os UI research (R1/R2/R3)

Reviewer: **R4** (fresh-mind, adversarial completeness). Posture: refute, don't help.
Date: 2026-07-15. Inputs: only `R1-best-practices.md`, `R2-analogs.md`,
`R3-untold-requirements.md`. Every gap below names the evidence it traces to (an analog
failure, a standard, a demonstrable norm, or the product's own stated data model). I did
not read the codebase; where a claim is checkable against in-repo files I say so, because
that checkability is itself the indictment.

**Headline finding:** the user's *first-named* mechanic — **SKILLS INSTALLED** — has
**no research behind it at all** (no best-practice target, no analog, no requirement),
and the two adjectives that define the whole product — **"intuitive"** and
**"visionary / cutting-edge"** — are each backed by essentially nothing concrete. This
is the exact failure the prior PRD caught: the headline capability researched only in
name while its sub-parts got the attention.

---

## Q1 — Which requirement CATEGORY is missing entirely?

### 1A. SKILLS INSTALLED — the headline mechanic, entirely unresearched (CRITICAL)

The token `skill` appears **exactly three times** in all three files, and not one is
research on the mechanic:

- `R2:13` — the header *promises* to serve it: "Our surfaces to serve … **skills
  installed** · tokens … Read every analog below against those four." Then R2 supplies
  **zero analogs** for skills-installed. All seven analogs (LangSmith, Langfuse, Airflow,
  Temporal, GitHub Actions, token meters, AutoGPT/LangGraph) serve tokens, running-runs,
  or %-to-goal. The doc names the surface and then never returns to it.
- `R1:120` and `R1:192` — "skills" appears only as a generic *panel slot* ("skills,
  tokens, queue, active-run, progress … ~4 primary panels + a sidebar") that needs
  empty/stale states. That is layout arithmetic, not research.

**What is missing:** how to *visualize an installed-skills/agents/tools inventory* — what
a "skill" even is to the operator (a `SKILL.md`? a slash-command? an installed plugin?),
its version/provenance, enabled/disabled state, which skills a given run actually
*invoked*, staleness ("skill changed since last run"). None of this is touched.

**Evidence it's a real gap, not invented:** obvious, directly-analogous prior art exists
and was skipped — VS Code Extensions view, Obsidian community-plugins pane, Raycast
extension list, Home-Assistant integrations, npm/pip inventories, and Claude Code's own
`/plugins` + skills list. An inventory-management UX is a solved genre; R2's own method
("find analogs for each surface") demanded one here and delivered none. This is the
single largest hole and it sits on the mechanic the user listed **first**.

### 1B. "INTUITIVE" — onboarding / learnability, entirely unresearched (HIGH)

The product statement's load-bearing verb is "making the system a lot more **intuitive**."
Grep for `onboard|tutorial|tooltip|glossary|guided|teach|walkthrough|first-time|learn`
returns **no substantive hit** (only a `learn.microsoft.com` URL and a `mobbin/glossary`
URL — neither about user education).

- R1 Target 6 and R3 §3 cover **empty / first-run states** — but "no data yet" is *not*
  onboarding. Nothing covers how a first-time operator *learns the mental model*: what
  maker → verifier → land-gate → write-back means, what "criteria_passing" is, what a
  token budget is, how to read the state machine. No progressive disclosure, no
  contextual help/tooltips, no glossary, no guided first-run tour.
- R3-R3.1 ("not initialized → guidance on how to init") is the *only* sliver, and it
  covers one CLI step, not comprehension.

**Evidence:** "intuitive" is the user's explicit success word; learnability/onboarding is
a first-order UX category (Nielsen's "learnability" heuristic) that the research treats
as out of scope by omission. A dashboard can be data-complete and still fail the
"intuitive" bar it was commissioned to hit.

### 1C. "VISIONARY / CUTTING-EDGE" — no concrete interaction/visualization research (HIGH)

Success criterion A4 is "daily-driver **and** visionary," and the user asked for a
"cutting edge" UI. The only concrete backing:

- R1 Target 8 = **motion timings** (150–200ms ease-out) — table-stakes polish.
- R1 Target 10 = **dark-mode aesthetics** (true-grey, one accent) — table-stakes polish.

Neither is a *cutting-edge interaction or visualization paradigm*. There is no research on
novel agent-state visualization, spatial/graph/temporal metaphors beyond a generic "flow
chart" borrow (R1-2.2, imported from Datadog's *multi-agent* product — see Q4), no
information-architecture concept that would make this feel visionary rather than "a tidy
dark dashboard." "Visionary" is silently reduced to "smooth transitions + dark theme,"
and then actively *undercut* by R1-10.3 (see Q4 contradiction). The ambition the user
paid for has no design research under it.

### 1D. MULTI-GOAL / PORTFOLIO progress — only single-goal % was researched (MEDIUM)

The user said "**running projects** [plural], **their** state in % vs the project goal."
All progress research (R1 Target 4, R3 §8) defines % for **one** goal
(`criteria_passing/criteria_total`). No research on the *portfolio* view the plural asks
for: many goals each at their own %, a roll-up/aggregate, ranking, or how the home screen
renders "3 goals running, one at 4/6, one at 0/5, one crashed." This is the natural home
of Mechanic 3 (running projects) and it went unmodelled. (Ties to the single-pane gap in
Q3.)

### Well-covered categories (stated briefly, per the rules)

Tokens (R1-T3, R2-#6), single-goal progress-honesty (R1-T4, R3-§8), concurrency/torn-read
integrity (R1-1.5, R3-§1), stale/crash liveness (R3-§2), accessibility (R1-T5, R3-§7),
and localhost security incl. DNS-rebinding (R1-T9, R3-§5) are genuinely thorough. No
complaint there.

---

## Q2 — Which claims have NO source / weak source doing load-bearing work?

Every claim carries a tag, so none is *untagged*. The problem is **[REPORTED] and
[ASSUMPTION] tags propping up load-bearing structure that a [VERIFIED] should hold:**

1. **R1-6.1 — the "92% no empty state / 78% no error state / 100% generic spinner"
   statistic.** Tagged `[REPORTED https://blog.vibecoder.me/...]`, a single blog that
   attributes the numbers to an unlinked "2025 NN/g analysis of 50 dashboards." A striking
   figure laundered through a secondary blog, with the claimed primary never produced —
   yet it is the sole justification for "treat empty/loading/error/offline/first-run as
   required deliverables with their own acceptance criteria." A [REPORTED] doing a
   [VERIFIED]'s job.

2. **R1-1.5 — write-temp-then-atomic-rename, the central data-integrity fix.** The entire
   torn-read defense (and R3-R1.2) rests on this, but it is `[REPORTED]` twice
   (atomically GitHub, LWN) with no primary/authoritative citation for the *Windows*
   behavior that actually matters here. R3-R1.3 partially rescues it (Go issue, MSDN
   forum — also `[REPORTED]`), but the most load-bearing technical requirement in the PRD
   is built on secondary sources and archived forum posts.

3. **R1-3.1 / 3.2 / 3.3 — the whole token-visualization primitive set.** All `[REPORTED]`
   from vendor/marketing/OSS-readme blogs (llm-cost-dashboard readme, Broadcom docs,
   llmcosttracker, traceloop). Mechanic 2's *entire* design vocabulary (burn-down, budget
   gauge, per-run attribution, forecast-to-exhaustion) has no primary or independent
   source — it's what cost-tool vendors say about their own tools.

4. **R3-R2.1 — "`in_flight` with no `session_end` = crash marker."** `[ASSUMPTION]`, and
   the entire crash-detection feature depends on it. R3 itself lists it in the
   "Verification backlog" as unverified against the real `run-status.json` schema — a
   schema that lives in-repo and was never opened. Load-bearing assumption about the exact
   data the UI must read.

5. **R3-R6.1 / R6.2 / R6.3 — the write-path concurrency-safety design.** `[ASSUMPTION]`
   throughout: undo = git reset (R6.1), optimistic concurrency via "expected iter/SHA or a
   lease" and "whether the CLI exposes a lock/lease or a compare-and-set entry point"
   (R6.2), idempotency (R6.3). The *entire* control-surface safety model is speculation
   about a CLI locking/CAS capability R3 openly admits it never checked. If the CLI has no
   lease/CAS entry point, this whole section is unimplementable as written.

6. **R1-9.4 / R3-R5.4 — "don't re-leak already-scrubbed secrets."** `[ASSUMPTION]` on both
   sides ("No single canonical URL; general secure-logging practice"). A load-bearing
   *security* requirement resting on an unverified belief about what the scrub actually
   covers and what still reaches STATE.md / run-log / run-status on disk.

7. **R3-R10.3 / R10.4 — queue.json `consumed`-flag semantics and the
   `AGENTIC_OS_NOTIFY_CMD` event set.** Both `[ASSUMPTION]`. Queue rendering (Mechanic 3)
   and notification reconciliation depend on data-model facts that were never confirmed.

**Pattern:** R3's "Verification backlog" (its own lines 266–271) is a confession that the
requirements doc left the product's actual data model — run-status schema, writer
strategy, lock/lease model, scrub coverage, queue semantics, notify events — as open
assumptions, despite those files sitting in the same repo the researchers could grep. The
product context even proves the files *were* inspected once ("VERIFIED it is NOT
atomic-renamed"), which makes the un-verified remainder a choice, not a limitation.

---

## Q3 — Which analog's known failure is NOT covered by any requirement?

Cross-checking every R2 complaint against R1/R3 requirements. Most are answered (staleness
→ R3-R4.2/R2.2; version-fragility → R3-R10.2; whole-history load → R3-R9.2; NL-self-judged
"done" → R3-R8.1). The following failure modes are **not converted into any requirement**:

1. **LangGraph Studio: the browser blocks plain-HTTP localhost.** `R2:279` — Studio shows
   "Failed to load assistants" because "Safari blocks plain-HTTP traffic on localhost"
   (and Brave Shields do too), plus an Apple-Silicon-only platform trap. This is a failure
   where **the dashboard never loads at all.** R3 §5 (security) covers loopback bind, Host
   allowlist, CSRF — nothing about browser localhost-HTTP policy or browser compatibility.
   Worse, it **collides with R1-9.2**, which recommends "strong authentication, even if it
   is over unencrypted HTTP." On Windows-first the operator's default browser is Edge (and
   likely Chrome), whose localhost/secure-context policies are unaddressed. A proven,
   dashboard-killing analog failure with zero requirement. (Also a Q4 contradiction.)

2. **GitHub Actions: no single-pane view over many runs.** `R2:186` and R2 synthesis #6
   (`R2:316`) flag "an org-wide dashboard to see all workflows at once" as a *proven,
   still-requested* need, and R2's COPY line calls it a "proven need." Yet **R3 never makes
   it a requirement.** For a single-operator / many-goals product this is the home screen
   and the literal surface for Mechanic 3 ("running projects"). Identified as a need,
   never required, never designed (see also Q1-1D).

3. **Temporal: a single oversized PAYLOAD bricks the view.** `R2:143` — the history view
   throws when *one* fetched payload exceeds the gRPC cap (12MB vs 4MB). R3-R9.2 answers
   the *count* problem (virtualize/paginate *many* rows) but **not the per-record size
   problem**: one giant JSONL line (a full diff, a transcript, a stack dump) will stall a
   virtualized list, because virtualization recycles many small rows and does nothing for
   one huge one. R2's own AVOID ("keep big blobs behind lazy expand") was never mirrored
   into an R3 requirement.

4. **Token meters: opaque/mistrusted counts.** `R2:236` — users "suspected Claude Code
   limits were draining abnormally fast and couldn't tell why"; Cursor users "questioned
   whether token counts were inflated." No requirement makes the token number
   **auditable/explainable** — i.e., drill from a displayed total down to the run-log
   events that sum to it. R1-3.1 gives per-run *attribution* (which goal spent it) but not
   *derivation* (prove this number). Trust-in-the-meter is a distinct, uncovered failure.

5. **AutoGPT / Sentry: the runaway loop is a silent failure.** `R2:272`/`R2:276` — agents
   "loop endlessly, causing silent failures that only show up when users complain;
   traditional monitoring tools track uptime, not behavior." "no-progress" is *named* as a
   state node (R1-2.2) but **no requirement detects or surfaces a runaway** — e.g., N
   iterations with zero criteria change, or repeated identical verifier verdicts, → an
   alert. The bounded budget is not the same guard: a loop can burn its whole budget making
   no progress, and nothing is required to say so *while it happens*.

6. **Airflow: the live graph/flow view collapses at scale and DoSes the backend.**
   `R2:112`/`R2:116` — graph view "takes 2–3 minutes to load ~1k expansions," "API server
   becomes unresponsive … N+1 query storms." R3-R9.2 covers the *log list*; the proposed
   **run flow/timeline graph** (R1-2.2) has no scaling or query-budget requirement. Per-run
   the node count is small (4-node lifecycle), so this is lower severity — but *across many
   goals × many iterations* a portfolio timeline can grow, and no requirement bounds it.

---

## Q4 — Contradictions / scope traps / architecture-impossible assumptions

1. **"Visionary" vs. "calm restraint" — an unresolved contradiction that silently narrows
   the ask.** The user wants "cutting edge … visionary for **all** mechanics." R1-10.3
   pushes the opposite: "the most effective SaaS dashboards display between five and nine
   core elements," "whitespace and calm design outperform data-dense layouts." R1 waves at
   this ("Balances A4") but never resolves *how a design is simultaneously visionary and
   minimalist-restrained.* Combined with the total absence of visionary-viz research
   (Q1-1C), the aggregate output quietly reduces "visionary UI for all mechanics" to "a
   calm dark status dashboard with 150ms transitions" — precisely the "narrows the user's
   ask to a status table" trap. The tension must be named and adjudicated in the PRD, not
   averaged away.

2. **Replay assumes historical data the rewrite-in-place model may not retain.** R1-2.3
   (`R1:48`) requires "every maker/verifier iteration … inspectable after the fact
   (replay), not only live," and R2 endorses a "replayable timeline." But the product
   context states `run-status.json` is **rewritten in place per iteration** — so
   per-iteration criteria snapshots (the data behind "%-to-goal *over time*") are
   **destroyed on each rewrite** unless `run-log.jsonl` explicitly carries the full
   criteria state per iteration. No note verifies that it does. Replay of progress history
   may be architecturally unsupported, and the research assumed it into existence without
   checking. Load-bearing capability assumption vs. the documented data model.

3. **Plain-HTTP security posture vs. browsers that block plain-HTTP localhost.** R1-9.2
   explicitly blesses "strong authentication, even if it is over unencrypted HTTP," while
   R2's LangGraph analog shows browsers *refuse to load* plain-HTTP localhost. You cannot
   both "keep it simple over HTTP" and "reliably load in the operator's Windows browser."
   The resolution (HTTPS with a locally-trusted cert, or a secure-context exemption)
   reintroduces exactly the complexity HTTP was chosen to avoid, and is unaddressed.
   (Same evidence as Q3-1.)

4. **Multi-agent observability patterns imported into a single-threaded system.** R1-2.2
   (`R1:43`) borrows Datadog's flow chart of "**inter-agent** interactions" and LangSmith's
   agent "internal monologue." This product is **single-threaded: one maker → one
   verifier**, not an agent mesh. Modelling an inter-agent interaction graph over-scopes;
   the real object is a fixed 4-node lifecycle (maker → verifier → land-gate → write-back).
   Importing the mesh metaphor risks building visualization the architecture can't populate.

5. **Runaway-loop urgency imported from an architecture we don't have.** R2-#6 frames
   real-time token freshness as needed to "catch a runaway loop." But this loop is
   **bounded and single-threaded with its own budget stop** — it halts itself at the cap.
   The "catch it before it bankrupts you" panic is a multi-tenant-SaaS fear; here it's
   over-imported. Burn-down is still worth showing, but the framing over-states the risk
   the local architecture actually carries.

6. **Phase boundary is fuzzy: read-only-v1 vs. a fully-specified write path.** R3-R1.5
   mandates the UI be "strictly read-only on every CLI-owned file in v1," yet R3 §6
   specifies a full control surface (undo=git reset, optimistic concurrency, idempotency,
   audit) without clearly gating it to phase 2. A scope trap: control-surface complexity
   (CAS/lease/audit) can bleed into a v1 that was supposed to be read-only. The PRD must
   draw the phase line explicitly.

---

## Bottom line for the PRD authors

The integrity/accessibility/security *plumbing* is well-researched. The **product** is
not: the first-named mechanic (skills) has no research, and the two words that justify the
whole project ("intuitive," "visionary") have no research. The requirements doc left the
actual on-disk data model as unverified assumptions it could have checked in-repo, and two
analog-proven, dashboard-killing failures (browser blocks HTTP-localhost; no single-pane
multi-goal home) never became requirements. Close these before the PRD claims coverage.

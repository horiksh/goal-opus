# R2 — Analog Software with Similar Mechanics

**Focus:** products/OSS whose core mechanics resemble the agentic-os UI (agent-run
observability, running-project state machines, % vs goal, token budget vs spend,
localhost dashboards). For each: (a) core mechanics, (b) praise, (c) complaints WITH
source, (d) one line COPY / one line AVOID for our PRD.

**Priority = the COMPLAINTS.** They are the failure modes our dashboard must design
around. Every claim carries an epistemic tag:
`[VERIFIED+SRC <url>]` = primary source read · `[REPORTED <url>]` = secondary ·
`[ASSUMPTION]` = with verification path.

Our surfaces to serve (from product statement): **skills installed · tokens
available & used · running projects/goals · state in % vs goal.** Read every analog
below against those four.

---

## 1. LangSmith (LangChain) — LLM/agent trace & eval observability

### (a) Core mechanics
Records agent runs as nested **traces → spans** (each LLM/tool call is a span), shows
per-step inputs/outputs, latency, and **token + cost per step and per run**; plus
datasets, eval runs, and a prompt playground. Billing is trace-volume based.
`[REPORTED https://www.langchain.com/langsmith/observability]`

### (b) What users praise
- Deep step-by-step trace drill-down is the reason teams adopt it; treated as the
  reference model for "show me what the agent actually did."
  `[REPORTED https://www.zenml.io/blog/langfuse-vs-langsmith]`
- Fast queries/filters even as trace volume grows (vendor design claim).
  `[REPORTED https://docs.langchain.com/langsmith/observability]`

### (c) What users COMPLAIN about
- **Cost scales with telemetry, so teams sample away their own visibility.**
  "LangSmith customers routinely sample down to 0.1% of their actual traffic to keep
  costs manageable" — which "defeats the entire purpose of having observability" for
  probabilistic edge-case failures.
  `[REPORTED https://inference.net/content/langsmith-pricing/]`
- **Per-seat + overage pricing surprises.** Plus plan $39/seat/mo (5 engineers = $195
  before a single trace); trace overages $2.50/1k, and at 50M spans the overage alone
  "exceeds $4,900." `[REPORTED https://inference.net/content/langsmith-pricing/]`
- **Extended retention is a second meter** ($5.00/1k for 400-day retention past quota)
  — cost keeps accruing after the run is over.
  `[REPORTED https://pydantic.dev/articles/ai-observability-pricing-comparison]`

### (d) For our PRD
- **COPY:** the trace→span drill-down with per-step token+cost+latency inline — this is
  the gold-standard "what did the agent do this iteration" view.
- **AVOID:** any design that makes richer observability cost more, forcing the operator
  to throttle their own visibility. We are local + file-based → keep 100% of iterations
  visible, always. Sampling is our anti-pattern.

---

## 2. Langfuse — open-source, self-hostable LLM observability

### (a) Core mechanics
Same trace/observation/score model as LangSmith but self-hostable; backend is
**ClickHouse** for trace analytics + Postgres + Redis + S3/blob for ingestion.
`[VERIFIED+SRC https://langfuse.com/self-hosting/deployment/infrastructure/clickhouse]`

### (b) What users praise
- Self-host = own your data, no per-trace SaaS meter; the escape hatch teams pick when
  LangSmith cost/sampling bites. `[REPORTED https://www.zenml.io/blog/langfuse-vs-langsmith]`

### (c) What users COMPLAIN about — the self-hosting tax
- **Traces lag 12–24h behind real time.** User: "I'm seeing a huge lag in the traces
  show in the UI raging from 12-24 hours … need zero lag from the time ingested … to
  see in UI." Maintainer could name no single cause — blamed ClickHouse resourcing,
  ingestion-queue backlog, Redis/S3 contention.
  `[VERIFIED+SRC https://github.com/orgs/langfuse/discussions/9243]`
- **The analytics store is the bottleneck.** The Traces-page metrics query
  (`observationsAndScoresCTE`) "consistently appears at the top of system.processes and
  causes excessive CPU/IO/memory," even after optimizations.
  `[REPORTED https://github.com/langfuse/langfuse/issues/11383]`
- **Version-fragile:** upgrades break the UI — e.g. a missing `events` table makes the
  traces page throw "Internal error"; a ClickHouse 26.5 upgrade 500s the Scores page.
  `[REPORTED https://github.com/langfuse/langfuse/issues/11924]`
  `[REPORTED https://github.com/langfuse/langfuse/issues/14065]`

### (d) For our PRD
- **COPY:** the self-host / own-your-data ethos — we already win here (all state is
  local files under `.agentic-os/`, no external ingestion pipeline to lag).
- **AVOID:** standing up a heavy analytics DB (ClickHouse-class) behind a local
  dashboard. Their #1 pain (24h lag, version breakage) is an ingestion-pipeline pain we
  get to skip by reading `run-status.json` / `run-log.jsonl` directly. Do not reintroduce
  it. Read files → render; no ETL between the loop and the screen.

---

## 3. Apache Airflow — DAG-run orchestration UI (run state + graph)

### (a) Core mechanics
Grid/Graph views of a DAG's runs; each **task = a node with a color-coded state**
(queued/running/success/failed/skipped/up_for_retry); per-run drill into logs; manual
trigger, clear/retry. Best analog for "running projects + per-step state machine."
`[REPORTED https://github.com/apache/airflow/issues/26901]`

### (b) What users praise
- The color-coded state grid is the mental model people expect for "where is each run
  and which step failed"; asset/lineage-style views praised in orchestrator comparisons.
  `[REPORTED https://dev.to/isha_vason/orchestrating-our-way-out-of-chaos-how-i-compared-airflow-prefect-and-dagster-and-picked-what-23np]`

### (c) What users COMPLAIN about
- **Auto-refresh silently lies.** In graph view the "auto-refresh icon shows
  indefinitely that the page is refreshing but nothing happens"; grid refreshes, graph
  doesn't — you must hard-reload to see current task status.
  `[VERIFIED+SRC https://github.com/apache/airflow/issues/26901]`
- **Live views collapse at scale.** Graph view takes "2–3 minutes to load DAGs that have
  ~1k expansions" and the worker times out; new grid view is "very slow … on large DAGs."
  `[REPORTED https://github.com/apache/airflow/issues/27483]`
  `[REPORTED https://github.com/apache/airflow/issues/23772]`
- **The UI DoSes the backend.** "API server becomes unresponsive when viewing UI with
  many active DAG runs"; N+1 query storms only fixed in 3.1.2.
  `[REPORTED https://github.com/apache/airflow/discussions/58395]`

### (d) For our PRD
- **COPY:** color-coded per-step state (queued/running/pass/fail/retry) as the primary
  "run lifecycle" visual — maker → verifier → land-gate → write-back maps cleanly onto
  it.
- **AVOID:** a refresh indicator that spins without actually updating (destroys trust in
  a live dashboard). If we poll `run-status.json`, the spinner must reflect the *last
  successful read*, and stale data must be labeled stale — never shown as if live.

---

## 4. Temporal Web UI — durable-workflow run history

### (a) Core mechanics
Every workflow run is an append-only **Event History**; the UI renders the event
timeline + current state, input/output payloads, and pending activities. Closest analog
to our append-only `run-log.jsonl`. `[VERIFIED+SRC https://docs.temporal.io/web-ui]`

### (b) What users praise
- Append-only event history = fully replayable, auditable "what happened, in order" —
  the durability model teams choose Temporal for.
  `[REPORTED https://docs.temporal.io/web-ui]`

### (c) What users COMPLAIN about
- **Big payloads brick the history view.** UI throws when the fetched history exceeds the
  gRPC message cap — "messages larger than the max gRPC message limit (12224559 vs.
  4194304 bytes)" — making large-history workflows unviewable.
  `[VERIFIED+SRC https://community.temporal.io/t/the-workflow-history-in-the-ui-throws-error-with-max-grpc-message-limit/4114]`
- **History size directly degrades load time;** docs advise capping concurrent ops to
  "500 or fewer … to decrease the loading time in the Web UI," and offloading large
  payloads to external storage. `[VERIFIED+SRC https://docs.temporal.io/cloud/limits]`

### (d) For our PRD
- **COPY:** the append-only event-history timeline as the canonical per-run record (we
  already have `run-log.jsonl`) — render it as a scrollable, replayable timeline.
- **AVOID:** loading a whole run's history/payloads into one request. Our
  `run-log.jsonl` is append-only and grows unbounded → tail/paginate/virtualize it, and
  keep big blobs (diffs, transcripts) behind lazy "expand" links, not inline.

---

## 5. GitHub Actions run view — CI live logs & run status

### (a) Core mechanics
Per-run list of jobs → collapsible steps, each streaming **live logs** with status
icons; cancel/re-run; download logs. The reference for "watch a running job's log
stream." `[REPORTED https://github.blog/engineering/architecture-optimization/how-github-actions-renders-large-scale-logs/]`

### (b) What users praise / what GitHub had to engineer
- Rendering 50,000+ live log lines smoothly required **UI virtualization** (render only
  visible lines), a **custom virtualization lib**, **height estimation** instead of
  precise measurement, and **clustering lines in groups of 50** to cut DOM churn — fixed
  text-selection and mobile jank.
  `[VERIFIED+SRC https://github.blog/engineering/architecture-optimization/how-github-actions-renders-large-scale-logs/]`

### (c) What users COMPLAIN about
- **Live streaming silently stalls / truncates.** "Logs will not stream and only appear
  upon refreshing the browser" (Safari); logs stuck "at 1st line"; steps appear out of
  order; lines jump "from line 58 to line 200+."
  `[VERIFIED+SRC https://github.com/orgs/community/discussions/89879]`
- **Real-time + backscroll capped at ~4MB** — past that you must wait for the job to
  finish to see the rest. `[REPORTED https://github.com/orgs/community/discussions/127903]`
- **Large output freezes the browser.** "Job logs load very slowly and cause browser to
  freeze with a very large group output"; page freezes many seconds until all output
  dumps at once. `[REPORTED https://github.com/orgs/community/discussions/8848]`
- **No timing until done:** all pre-loaded lines "have the same timestamp," so you can't
  correlate events with real time mid-run.
  `[VERIFIED+SRC https://github.com/orgs/community/discussions/89879]`
- Requested but missing: **an org-wide dashboard to see all workflows at once** (single
  pane over many runs). `[VERIFIED+SRC https://github.com/orgs/community/discussions/89879]`

### (d) For our PRD
- **COPY:** virtualized, clustered log rendering for `run-log.jsonl` streaming, and a
  single top-level "all runs / queue" pane — both are proven needs.
- **AVOID:** naïvely dumping the full log into the DOM (freezes) and a stream that stalls
  without telling the user. If the tail can't keep up, show an explicit "stream paused /
  N new lines below" affordance rather than a silent stall.

---

## 6. Token / cost meters — Cursor, Claude Code, OpenAI usage dashboard

Directly serves our **"tokens available & used (budget vs spend)"** surface. Grouped
because the three share one dominant failure mode: **the meter is invisible until the
money's gone.**

### (a) Core mechanics
Subscription/credit budget + usage-based overage; a usage page (and for Claude Code a
`/usage` command) showing cumulative spend/tokens; some show per-model or per-day totals.
`[REPORTED https://docs.bswen.com/blog/2026-03-23-cursor-ide-pricing-transparency/]`

### (b) What users praise
- When surfaced *in the workflow*, an always-visible limit indicator is exactly what
  people want — a community script that "surfaces [Claude Code] limits on every message"
  was celebrated precisely because the native UI hides them.
  `[REPORTED https://www.xda-developers.com/claude-code-script-surfaces-usage-limits/]`

### (c) What users COMPLAIN about — the highest-value failures for us
- **Surprise four-figure bills from an unbounded agent.** Cursor users hit ~$2,000 bills:
  "The meter is running and there's no big flashing warning"; "the tool gives an
  autonomous loop an open-ended budget and no hard stop."
  `[VERIFIED+SRC https://dev.to/adioof/cursor-3-users-are-getting-2000-bills-nobody-read-the-pricing-page-2ako]`
- **"How much" but not "what caused it."** OpenAI's dashboard "answers how much while
  users need to know what caused it" — no per-feature/per-run attribution; billing
  history "doesn't show exactly where tokens went."
  `[REPORTED https://dev.to/hassann/how-to-track-openai-api-spend-per-feature-a-cost-attribution-playbook-2dm7]`
  `[REPORTED https://docs.bswen.com/blog/2026-03-23-cursor-ide-pricing-transparency/]`
- **Usage data lags tens of minutes to hours** — "too slow for runaway loops or hourly
  burn alerts"; users report the dashboard "taking 10 minutes to update or overnight … a
  massive downgrade from near-instant."
  `[VERIFIED+SRC https://community.openai.com/t/api-usage-dashboard-not-updating-updating-slowly/692234]`
  `[REPORTED https://dev.to/hassann/how-to-track-openai-api-spend-per-feature-a-cost-attribution-playbook-2dm7]`
- **Limits hidden by default, no passive indicator.** For Claude Code "the only way to
  check where you stand is by running `/usage` … Neither option gives you a passive,
  always-visible indicator … no warning that lives where you actually work."
  `[VERIFIED+SRC https://www.xda-developers.com/claude-code-script-surfaces-usage-limits/]`
- **Metering semantics are opaque/mistrusted:** users suspected Claude Code limits were
  draining abnormally fast and couldn't tell why; Cursor users questioned whether token
  counts were inflated.
  `[REPORTED https://thenewstack.io/claude-code-usage-limits/]`
  `[REPORTED https://medium.com/@jimeng_57761/when-cursor-silently-raised-their-price-by-over-20-and-more-what-is-the-message-the-users-are-6af93385f362]`

### (d) For our PRD
- **COPY:** an always-on, passive budget-vs-spend meter that lives where the operator
  works — with **per-run / per-iteration attribution** ("this iteration burned X tokens")
  and a projected burn/exhaustion estimate, not just a cumulative total.
- **AVOID:** the four canonical failures — (1) meter you must go look for, (2) totals
  with no per-run breakdown, (3) laggy numbers unfit for catching a runaway loop, (4) an
  agent loop with no visible hard cap. Since our loop is bounded and local, show the cap
  and the live burn-down against it, and read spend from the run log with ~real-time
  freshness.

---

## 7. Autonomous-agent "mission control" & local agent IDEs — AutoGPT, LangGraph Studio

Serves our **"state in % vs goal"** surface (goal-completeness) and the **localhost
dashboard** delivery model.

### (a) Core mechanics
AutoGPT: an autonomous loop that self-assesses whether the goal is "complete" and keeps
acting until it decides done. LangGraph Studio: a local agent IDE (`langgraph dev` →
localhost) to visualize/step a graph run.
`[REPORTED https://github.com/vectara/awesome-agent-failures/blob/main/docs/case-studies/autogpt-planning-failures.md]`
`[REPORTED https://docs.langchain.com/oss/python/langgraph/studio]`

### (b) What users praise
- LangGraph Studio's move to a **local server + web UI** (over the old desktop app) is
  praised for no-Docker startup, hot-reload, and cross-platform reach — validates the
  localhost-web-app delivery we're assuming.
  `[REPORTED https://docs.langchain.com/oss/python/langgraph/studio]`

### (c) What users COMPLAIN about
- **"Complete vs not" from natural-language self-judgment is unreliable** and "typically
  defaulted to 'more work needed'," driving runaway loops (hundreds of API calls, no
  final output). `[VERIFIED+SRC https://github.com/vectara/awesome-agent-failures/blob/main/docs/case-studies/autogpt-planning-failures.md]`
- **Silent failure with no behavioral observability:** "when AI agents fail, they can …
  loop endlessly, causing silent failures that only show up when users complain.
  Traditional monitoring tools track uptime, not behavior."
  `[REPORTED https://blog.sentry.io/ai-agent-observability-developers-guide-to-agent-monitoring/]`
- **Local dashboard = fragile localhost/browser edges:** Studio shows "Failed to load
  assistants" because "Safari blocks plain-HTTP traffic on localhost" (and Brave Shields
  do too); the desktop app was Apple-Silicon-only and got deprecated.
  `[REPORTED https://docs.langchain.com/oss/python/langgraph/studio]`
- Nx/Storybook-class local dashboards: **stale state without auto-rebuild** — devs
  "don't see the effect right away and need to manually rebuild," and unclear console
  errors on failure. `[REPORTED https://nx.dev/blog/storybook-watch-dependencies-nx]`

### (d) For our PRD
- **COPY:** measure "% vs goal" from the **rubric** (`criteria_passing / criteria_total`
  against a Default-FAIL rubric) — an *external, countable* signal — never from the
  agent's own "I think I'm done." This is our structural advantage over AutoGPT's
  self-judgment; make the % obviously rubric-derived and show which criteria are still
  failing.
- **AVOID:** localhost/browser fragility (test our http-on-localhost path on the
  operator's actual Windows browser), stale un-refreshed state, and any "done" signal
  that isn't traceable to a passed criterion. On Windows-first + solo operator, don't
  ship an Apple-Silicon-style platform trap.

---

## Cross-analog synthesis — the failure modes our dashboard must design around

1. **Stale-but-looks-live is the cardinal sin.** Airflow's spinning-but-dead refresh,
   GitHub's silently-stalled stream, OpenAI/Langfuse minutes-to-24h lag. A live dashboard
   that shows old data as current destroys trust faster than showing nothing. Our edge:
   read local files → label freshness explicitly; if a poll fails, say so.
2. **The meter must be passive, in-context, per-run, and real-time.** Every token/cost
   analog fails on at least one of those; nail all four (we read spend from a local run
   log, so we can).
3. **Observability must not have a cost/scale tax.** LangSmith sampling, Langfuse
   ClickHouse lag, Temporal payload caps, Airflow N+1, GitHub 4MB/freeze — all are
   "richer view = worse performance/cost." Local + file-based lets us keep 100% of every
   iteration visible; don't reintroduce an ETL/analytics tier.
4. **"% vs goal" must be rubric-derived, not self-assessed.** AutoGPT's central failure.
   Ours = `criteria_passing/criteria_total`, Default-FAIL — surface it as such.
5. **Virtualize the timeline/logs; paginate history; lazy-load big blobs.** GitHub had to;
   Temporal/Airflow break where they didn't. `run-log.jsonl` grows unbounded → design for
   it from day one.
6. **Provide the single-pane "all runs / queue" view** GitHub users still ask for — for a
   solo operator it's the home screen (queue.json + each run's lifecycle %).

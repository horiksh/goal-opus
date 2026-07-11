# R3 — Untold requirements (domain-mined)

> Single-agent mining pass over R1 (`R1-best-practices.md`) + R2 (`R2-analogs.md`) for the
> `/deep-prd "an agentic OS for this repository setup"` run. Every requirement below is one the
> **user did not state** but the evidence says a portable, Claude-Code-native, self-improving
> multi-agent "agent home" needs. Nothing here is invented: each traces to an R1/R2 verified/
> reported claim (with its underlying source URL), a durable-workflow standard, or a demonstrable
> user norm. Requirements that only EXTEND an existing repo mechanism say so explicitly.
>
> Tags (same convention as R1/R2, never upgraded): `[VERIFIED+SRC <url>]` = rests on a claim that
> survived R1's 3-vote adversarial verify · `[REPORTED <url>]` = rests on a primary-source claim
> below the verify cut (R2's limit-truncated set) · `[ASSUMPTION]` = the leap from evidence to
> requirement is inferential/normative; verification path stated inline (usually R4 gap-check or a
> user confirm).
>
> Scope guard: v1 "done" = a RUNNABLE orchestration layer coordinating goal-opus-style runs over
> shared file memory, portable, solo-operator, Windows/Claude-Code runtime. Portability is a design
> constraint, not a v1 gate. Retrieval is settled (primitives-first; no RAG/code-graph) — not mined.

---

## A · Empty / error / offline / first-run states

**U1 — Explicit first-run bootstrap phase, separate from the run phase, that scaffolds a fresh
agent home into a repo with no `.claude/` yet.**
The OS cannot assume STATE.md, `memory/`, agent defs, and a seeded rubric already exist; it needs an
initializer that creates them, makes the first git commit, and *verifies the agent/skill registry
refreshed before the first goal runs*. R1 documents an initializer agent that sets up on first run
(`init.sh`, a progress log, an initial git commit) as a distinct role. The repo's own STATE.md
Lessons prove the sharp edge: agent defs created mid-session are "not IMMEDIATELY spawnable"
(`Agent type 'goal-maker' not found`) and infra must exist BEFORE the session that uses it.
`[VERIFIED+SRC https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]`
Implication: PRD/roadmap must include an `init`/bootstrap command with a post-init registry-refresh
check as a hard gate before any goal loop.

**U2 — Precondition check that the TARGET is a git repo, with a defined failure/`git init` path.**
Durable state (progress log + commits) and multi-agent lock-claiming both depend on git; a TARGET
that is not a git repo silently breaks checkpointing and resumability. R1 makes plain-file + git the
sole cross-session persistence; R2's C-compiler lock-claiming is git-sync-driven.
`[VERIFIED+SRC https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]`
`[REPORTED https://www.anthropic.com/engineering/building-c-compiler]`
Implication: PRD must specify a git-precondition gate on every TARGET (offer `git init` or refuse
with a clear error) — not assume a git repo.

**U3 — Defined empty-queue / no-goal-in-flight idle behavior (clean no-op exit, never a spin).**
The orchestration layer needs a specified state for "nothing to do." R1's headless loop exits when
the contract has nothing failing, a cycle makes no changes, or a budget hits; R2's Airflow analog
(`stuck-queued tasks`) shows an undefined idle/queued state is a real production failure mode.
`[VERIFIED+SRC https://github.com/anthropics/cwc-long-running-agents]`
`[REPORTED https://github.com/apache/airflow/issues/56045]`
Implication: PRD must define the empty-queue exit condition as a first-class run state.

**U4 — Survive a mid-run API/offline/rate-limit stall and resume from file state, tagged
`paused`, not `failed`.**
An autonomous loop that treats a transient limit as a terminal failure loses the run. The repo's own
deep-research recovery lesson generalizes: read the file state, resume from cache, don't re-fire.
STATE.md Lessons: the rolling session limit needs real idle hours; `resumeFromRunId` replays
completed work for free (59k vs ~2M tokens).
`[VERIFIED+SRC https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]`
`[ASSUMPTION]` — that the orchestration layer (not just deep-research) needs this is inferential;
verify in R4 that no run-loop step assumes an always-available API.
Implication: PRD needs a distinct `paused/rate-limited` run state + resume-from-checkpoint, separate
from the abort/fail path.

---

## B · Data lifecycle (memory)

**U5 — A memory-growth guard / consolidation trigger for STATE.md + `memory/` (the "dreaming" gap).**
R1's biggest memory gap: no surviving claim substantiates an automated consolidation loop, and
context rot is *measured* — recall degrades as tokens grow "across all models." The repo rejected a
cron dreaming tool (D8) but that left unbounded append-only growth unsolved; a size/section-count
threshold that triggers a consolidation pass is still required or growth silently erodes retrieval.
`[VERIFIED+SRC https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents]`
`[ASSUMPTION]` — exact trigger (size threshold vs manual checkpoint vs scheduled) unresolved; hand to
R4/PRD to pick a mechanism or explicitly defer with a stated growth cap.
Implication: PRD must name a consolidation trigger (even a manual size-threshold prompt) rather than
assume Phase-6 write-back alone keeps memory readable.

**U6 — Memory export / backup / migration as plain-file copy, called out explicitly.**
Memory is the compounding asset; a portable framework the user moves between machines/homes needs a
stated export path. R1 establishes local-file portability as the norm (Agent-Teams task list
"persists locally, never uploaded," survives resume).
`[VERIFIED+SRC https://code.claude.com/docs/en/agent-teams]`
`[ASSUMPTION]` — that the user needs export/backup is a norm-based inference; confirm scope with user.
Implication: PRD should specify memory = plain files, export/backup = git/copy, and state it (so a
future format change doesn't strand memory).

**U7 — Memory deletion / redaction / scrub path (secrets or sensitive TARGET data leaked into memory).**
Secrets must never be in memory files, but leaks happen; the operator needs a way to redact/scrub and
delete. Context-08 mandates secrets stay in the credential layer, "never in prompts or memory files,"
and "delete sessions when done." D2 already makes memory a reviewable git diff — extend with a scrub
command.
`[VERIFIED+SRC https://www.anthropic.com/engineering/harness-design-long-running-apps]` (safety
posture; underlying norm from context-08 + R1 credential handling)
`[ASSUMPTION]` — leak-into-memory risk is real but the scrub UX is a design choice; verify in R4.
Implication: PRD needs a redaction/scrub procedure + a pre-write secret guard on memory files (see U21).

**U8 — Schema version field + migration for STATE.md sections and `criteria.json`, so upgrades don't
strand existing homes.**
The framework will change its state schema and rubric JSON as it upgrades; every installed agent home
must migrate rather than break. R1 flags version-pinned specifics drift (`/goal` v2.1.139+, teams
v2.1.178+); the Temporal durable-workflow analog makes versioning/idempotency a first-class concern.
`[VERIFIED+SRC https://code.claude.com/docs/en/agent-teams]`
`[REPORTED https://github.com/temporalio/rules]` (TMPRL1100 workflow-versioning)
Implication: PRD must add a schema-version field to STATE.md + criteria.json and a migration step in
the upgrade path (U26).

---

## C · Observability & watchability of long/looping runs

**U9 — A machine-readable run-status artifact (current iteration, criteria pass count, tokens spent)
the operator can tail — the observability floor.**
R1's gap #3: no primary source describes a control-plane/dashboard; is tail/watch the ceiling? For a
solo operator watching a multi-hour loop, a structured status file is the minimum. The practitioner
pattern (hooks → server → SQLite → dashboard) shows the shape but is reported-only.
`[REPORTED https://github.com/disler/claude-code-hooks-multi-agent-observability]` (R1 gap #3)
`[ASSUMPTION]` — that a status file (not a full dashboard) is the right v1 ceiling; decide in PRD.
Implication: PRD should specify a tailable run-status file per run; defer any dashboard/control-plane.

**U10 — A structured per-iteration run log (what changed, verdict, evidence pointers) a fresh session
can rehydrate from — extend STATE.md's `Last session` into a per-iteration orchestration log.**
R1 names the progress-log-alongside-git-history as "the key mechanism" for a fresh-context agent to
understand state. STATE.md today carries a prose `Last session`; the orchestration layer needs a
structured, appended-per-iteration log so a resumed run knows exactly where it stopped.
`[VERIFIED+SRC https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]`
Implication: PRD needs a per-goal, per-iteration run-log artifact (extend, not invent) feeding U30
resumability.

**U11 — First-class kill-switch and mid-run steer sentinel files (`AGENT_STOP`, `STEER.md`).**
A long/looping autonomous run needs a human off-ramp that doesn't require killing the process. R1
names `AGENT_STOP` (kill switch) and `STEER.md` (mid-run redirect) as documented backstops alongside
the progress log.
`[VERIFIED+SRC https://github.com/anthropics/cwc-long-running-agents]`
`[VERIFIED+SRC https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]`
Implication: PRD must include stop + steer sentinel files as run controls the orchestrator polls each
iteration.

---

## D · Rate / perf / cost floors and guards

**U12 — An aggregate iteration/goal budget at the ORCHESTRATOR level, above goal-opus's per-goal
`max_iterations`.**
goal-opus already bounds a single goal (validated against the Ralph-loop mandate). The NEW v1
orchestration layer coordinating many runs needs its own global bound, or a queue of goals can run
unbounded even though each goal is individually bounded. R2: Ralph docs *mandate* `--max-iterations`;
`--completion-promise` is a footgun (can't express SUCCESS vs BLOCKED).
`[REPORTED https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum]`
Implication: PRD must add an orchestrator-level global iteration/goal budget (extend the per-goal bound
upward).

**U13 — Cumulative token/cost surfacing + a budget stop condition.**
Cost is a real failure axis: multi-agent uses ~15× chat tokens and token usage alone explains 80% of
performance variance; the C-compiler run cost ~$20k over 2 weeks (~2B input tokens). The OS must
surface cumulative spend per run and stop on a budget.
`[VERIFIED+SRC https://www.anthropic.com/engineering/multi-agent-research-system]`
`[REPORTED https://www.anthropic.com/engineering/building-c-compiler]`
Implication: PRD needs a token/cost budget as an explicit stop condition, with cumulative spend shown
in the run-status file (U9).

**U14 — A fan-out justification gate: the orchestrator stays single-threaded by default and
parallelizes only for high-value, decomposable, breadth-first work.**
Multi-agent is benchmarked +90.2% but ~15× tokens; Agent-Teams cost scales linearly with active
teammates → cost-ineffective for routine/sequential work; Cognition's contrarian "Don't Build
Multi-Agents" argues for single-threaded + context-compression by default.
`[VERIFIED+SRC https://www.anthropic.com/engineering/multi-agent-research-system]`
`[REPORTED https://code.claude.com/docs/en/agent-teams]`
Implication: PRD must encode a decision rule for when the orchestrator fans out vs stays single-agent
— fan-out is opt-in per task, not the default.

**U15 — A no-change / no-progress stop detector, distinct from success and abort.**
A loop that iterates without changing anything is stuck and burning budget. R1's headless loop exits
when "a cycle makes no changes"; R2's Ralph loop documents the blocker surfacing after ~15 iterations.
`[VERIFIED+SRC https://github.com/anthropics/cwc-long-running-agents]`
`[REPORTED https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum]`
Implication: PRD needs a no-progress stop condition (e.g., empty diff / unchanged criteria N
iterations) as its own run outcome.

---

## E · Concurrency / collision safety

**U16 — File-ownership partitioning of the shared agent home when >1 run is active
(who may write STATE.md / `memory/`).**
The agent home is shared mutable state; concurrent runs writing STATE.md or `memory/` overwrite each
other. R2: concurrent same-file edits cause overwrites → partition file ownership (give each teammate a
disjoint file set).
`[REPORTED https://code.claude.com/docs/en/agent-teams]`
Implication: PRD must define write-ownership of shared-home files (or serialize STATE.md writes) before
allowing concurrent goals.

**U17 — A lock-file claiming protocol for any parallel task pull.**
If the orchestrator ever parallelizes, tasks must be claimed via locks so two agents don't grab the
same one. R2's C-compiler used lock files in `current_tasks/` with git sync forcing a second claimant
elsewhere; R1's Agent-Teams task claiming "uses file locking" to prevent races.
`[REPORTED https://www.anthropic.com/engineering/building-c-compiler]`
`[VERIFIED+SRC https://code.claude.com/docs/en/agent-teams]`
Implication: PRD needs a lock-claim protocol for the shared task list (only relevant once U14 permits
fan-out).

**U18 — A stuck-task / status-lag guard (completion timeout + reconciliation).**
Agents sometimes fail to mark tasks complete, deadlocking dependents; and resumed sessions can message
teammates that no longer exist. The task list needs completion verification + a stuck-task timeout.
`[VERIFIED+SRC https://code.claude.com/docs/en/agent-teams]`
`[REPORTED https://github.com/apache/airflow/issues/56045]` (stuck-queued analog)
Implication: PRD must add status reconciliation / stuck-task timeout to the task-list design.

**U19 — A decomposability check before any fan-out (fall back to single-agent on non-decomposable
work).**
Naive parallelism fails on a single non-decomposable task: in the C-compiler build every agent hit the
same bug, fixed it, and overwrote each other until the work was re-decomposed into per-file parallelism.
`[REPORTED https://www.anthropic.com/engineering/building-c-compiler]`
Implication: PRD's decomposition step must verify a task is actually decomposable before parallelizing,
else run single-agent (pairs with U14).

---

## F · Abuse / safety vectors

**U20 — A prompt-injection defense posture for researched/TARGET content (tool output is data, not
instructions).**
The `/prd` research phase and any goal that reads web pages or TARGET files ingest untrusted text that
may contain embedded instructions. R1: in auto mode the classifier "treats a relayed approval claim as
untrusted input," with an input-layer prompt-injection probe.
`[VERIFIED+SRC https://code.claude.com/docs/en/agent-teams]`
`[REPORTED https://www.anthropic.com/engineering/claude-code-auto-mode]`
Implication: PRD must state an untrusted-content boundary (observed content ≠ instructions) for the
research phase and TARGET reads.

**U21 — A structural secrets guard: secrets never enter memory files or inter-agent file messages.**
Inter-agent coordination is file-based (one agent writes, another reads) and memory is plain files;
either can accidentally capture a secret. Context-08: keep secrets in the credential layer, "never in
prompts or memory files."
`[VERIFIED+SRC https://www.anthropic.com/engineering/harness-design-long-running-apps]` (file-as-message-bus)
plus the credential-handling norm (context-08).
Implication: PRD needs a secret-handling rule + a pre-write scrub/guard on memory and message files
(pairs with U7 redaction).

**U22 — Classifier-decline detection + fallback routing, so a decline is never retried as an error.**
A frontier model may decline in security or bio/chem domains; in an autonomous loop a silent decline
looks identical to a real error and the loop retries forever. Context-08: route such tasks to a
fallback model (Opus) or a human, don't treat a decline as a retryable failure.
`[VERIFIED+SRC https://www.anthropic.com/engineering/harness-design-long-running-apps]` (safety-boundary
principle; detailed in context-08)
`[ASSUMPTION]` — decline-signature detection is a design task; verify feasibility in R4.
Implication: PRD must include decline-detection + fallback/human-escalation as a distinct branch, not a
retry.

**U23 — Role-scoped least-privilege tool allowlists, and no blind propagation of
`--dangerously-skip-permissions`.**
The verifier must stay read-only (no Write/Edit); teammates inherit the lead's permissions including
skip-permissions, and prefix-based deny rules are bypassable by chaining/wrapping
(`Bash(rm -rf *)` deny doesn't stop `cd /tmp && rm -rf foo`). The OS must enforce per-role boundaries
and not propagate skip-permissions into child runs unexamined.
`[VERIFIED+SRC https://code.claude.com/docs/en/agent-teams]`
`[VERIFIED+SRC https://code.claude.com/docs/en/hooks]`
`[REPORTED https://code.claude.com/docs/en/permissions]` (prefix-deny bypass)
Implication: PRD must specify per-role tool allowlists (verifier read-only) + a caution that prefix
denies are not a security boundary.

---

## G · Portability seams for "any repo" on Windows

**U24 — A defined install mechanic per artifact type: NTFS junction for self-editing skills, copy for
non-self-editing agent files, with a Windows fallback when junctions are unavailable.**
R1's gap #2: symlink-vs-copy had NO surviving primary claim; the repo's D2 already decided junctions
(copies fork the self-editing skill) but that is externally unverified and junction creation can fail
on Windows without privilege. Portability requires this be explicit, not implicit.
`[VERIFIED+SRC https://github.com/anthropics/claude-code/blob/main/plugins/README.md]` (plugin is the
packaging unit; the junction/copy split is R1 gap #2 + STATE.md D2)
`[ASSUMPTION]` — junction-vs-copy correctness on target Windows setups is unverified; verify with a real
install test in R4/build.
Implication: PRD must specify the install mechanic per artifact + a fallback path when junctions can't
be created.

**U25 — Defined user-level (`~/.claude`) vs project-level (`.claude/settings.json`) merge/override
precedence.**
R1's gap #2: the precise merge semantics are unresolved and matter specifically for a solo-dev Windows
setup. The OS installs into one or both and must state which config wins. Plugins can be pinned
declaratively in project-level settings.json ("shared with all collaborators").
`[VERIFIED+SRC https://code.claude.com/docs/en/plugin-marketplaces]` (project-level settings.json
pinning; merge semantics = R1 gap #2)
`[ASSUMPTION]` — exact precedence must be confirmed against Claude Code docs in R4.
Implication: PRD must specify config-merge precedence and where the framework installs (home vs
project).

**U26 — Install / uninstall / upgrade lifecycle commands for the framework.**
Portability isn't just first-run: adopting the OS into any repo requires a clean install, a clean
uninstall, and an upgrade path (which must run the U8 schema migration). R1: the plugin is the official
packaging unit, installable via `/plugin` or a committed settings.json; version drift is expected.
`[VERIFIED+SRC https://github.com/anthropics/claude-code/blob/main/plugins/README.md]`
Implication: PRD/roadmap must include install + uninstall + upgrade as named lifecycle operations
(upgrade invokes U8 migration + U24 junction rule).

**U27 — Dual-shell script + path portability (PowerShell and Git-Bash), since v1 hook/init scripts are
POSIX but the runtime is Windows.**
R1's harness ships `init.sh` and Bash hook scripts; the locked v1 runtime is Windows PowerShell +
Git-Bash. The repo's D3 already carved "Windows hook scripting gets its own tested step." Every script
and path the OS emits must work under both shells (or be shell-detected).
`[VERIFIED+SRC https://github.com/anthropics/cwc-long-running-agents]` (POSIX init/hook scripts; Windows
runtime = locked scope + STATE.md D3)
Implication: PRD must require dual PowerShell/Git-Bash handling for all emitted scripts and
path-separator normalization.

---

## H · Scheduling / event-triggered autonomy (R1's single biggest gap)

**U28 — A decided scheduling posture for v1: name the trigger surface (interval `/loop` now; cron /
webhook / GitHub-event routines as documented-future) rather than leave it implicit.**
R1's gap #1 and biggest gap vs the brief: scheduling/event-triggered autonomy is UNANSWERED by verified
claims — `routines.md` was fetched but no claim survived verification. A "self-improving home" implies
unattended triggers (nightly eval re-run, on-merge learn), but the evidence for cron/webhook/GitHub
routines is reported-only.
`[REPORTED https://code.claude.com/docs/en/routines]` (three trigger types: cron, on-demand API,
GitHub events — R1 gap #1)
`[ASSUMPTION]` — whether v1 ships any scheduler or defers to `/loop` is a scope decision; force it in
the PRD rather than leave it unaddressed.
Implication: PRD must explicitly decide v1 scheduling scope (likely `/loop` in, cloud routines
documented-future) — the biggest gap must be named, not silently dropped.

**U29 — Run durability across laptop sleep for long local runs (a closed/asleep laptop must not lose
the run).**
Context-04 lists "decouple compute from the laptop" as table stakes so a closed laptop doesn't kill the
run; cloud routines run on managed infra with the laptop off. Since cloud execution is out of the v1
Windows-local scope, v1 must at minimum make a run resumable after an interruption (feeds U30).
`[VERIFIED — talk]` context-04 (decouple compute); `[REPORTED https://code.claude.com/docs/en/routines]`
(cloud-hosted alternative)
`[ASSUMPTION]` — v1 answer is local resumability, not cloud; confirm in PRD scope.
Implication: PRD should acknowledge laptop-sleep interruption and make local resumability (U30) the v1
answer, with cloud routines as the documented scale-out.

---

## I · Failure recovery & resumability

**U30 — Crash-mid-loop resumability: detect a partial run and resume from the last git checkpoint +
run log + locked contract, never restart from zero.**
Durable state (git commits + progress log + locked default-FAIL contract) exists precisely so a
fresh/crashed context can resume; R1 names a `commit-on-stop` Stop hook as the backstop. The very PRD
run this file belongs to resumed across three sessions after rate-limit crashes — proof the pattern is
load-bearing. Temporal/durable-execution is the analog standard.
`[VERIFIED+SRC https://www.anthropic.com/engineering/harness-design-long-running-apps]`
`[VERIFIED+SRC https://github.com/anthropics/cwc-long-running-agents]` (commit-on-stop)
`[REPORTED https://vadim.blog]` (durable execution for LLM agents)
Implication: PRD needs a resume protocol (detect partial run → resume from last checkpoint) as a
first-class run state alongside success/abort/paused.

**U31 — Idempotent re-run steps, so a resumed run never double-applies write-back or criteria flips.**
Resumability is unsafe without idempotency: replaying a step after a crash must not double-count. The
Temporal/Airflow durable-workflow analogs make idempotency the core correctness property for replayable
workflows.
`[REPORTED https://github.com/temporalio/rules]` (TMPRL1100)
`[REPORTED https://vadim.blog]` (durable execution for LLM agents)
Implication: PRD must require write-back, criteria-flip, and memory-append steps be idempotent (safe to
replay on resume).

**U32 — Guaranteed write-back on crash/cancel at the ORCHESTRATOR level (not just per-goal Phase 6).**
The compounding contract (CLAUDE.md "write before walking") requires write-back on success, abort, AND
cancel — but a crash mid-loop can lose the lesson. goal-opus enforces Phase-6 write-back per goal;
the untold extension is that the orchestrator must guarantee write-back even when a *child goal*
crashes, via a commit-on-stop hook at the orchestration layer.
`[VERIFIED+SRC https://github.com/anthropics/cwc-long-running-agents]` (commit-on-stop Stop hook)
plus CLAUDE.md compounding-contract invariant.
Implication: PRD must specify a crash-time / cancel-time write-back guarantee at the orchestrator level
(extend Phase-6 upward).

---

## Highest-leverage untold requirements (the shortlist that most changes the product)

These 7 reshape the roadmap most; the rest are guardrails around them.

1. **U28 — Decide the scheduling posture.** R1's single biggest gap vs the brief. A "self-improving
   home" that never runs unattended is just a manual loop; the PRD must name what triggers v1 (even if
   the answer is "just `/loop`, routines documented-future").
2. **U1 — First-run bootstrap + registry-refresh gate.** Without a real init phase the "turn any repo
   into an agent home" promise doesn't start; the repo's own mid-session-registration failure proves
   it must be separate and verified.
3. **U30 + U31 — Crash resumability with idempotent steps.** The product runs long autonomous loops on
   a solo operator's Windows laptop; the deep-research crashes in this very run show non-resumable ≠
   viable. This is the difference between a demo and a system.
4. **U13 + U12 — Cost surfacing + an orchestrator-level budget.** The $20k C-compiler and 15×-token
   multi-agent figures make an unbudgeted OS a financial liability; a solo operator needs a hard cost
   ceiling and visibility.
5. **U24 + U25 — Windows install mechanic + config-merge precedence.** These are R1's gap #2 and the
   literal portability seam for the locked Windows-first scope; get them wrong and "any repo" adoption
   fails on the first install.
6. **U14 + U19 — Fan-out justification + decomposability gate.** Whether the orchestrator is
   single-threaded-by-default or multi-agent-by-default is the central architecture fork; the evidence
   (Cognition contrarian, linear teammate cost, non-decomposable C-compiler failure) says single-thread
   by default, fan-out opt-in.
7. **U11 + U9 — Kill-switch/steer sentinels + a tailable run-status file.** The minimum an operator
   needs to trust an autonomous loop: a way to watch it and a way to stop/redirect it without killing
   the process.

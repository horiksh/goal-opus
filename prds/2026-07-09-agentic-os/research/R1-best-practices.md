# R1 — Newest best practices + cutting-edge blueprints

> Deep-research sweep (mode: **deep**, via the `deep-research` workflow). Run `wf_5b9d8d17-fe1`.
> Pipeline: 6 angles → 26 sources fetched → 130 claims extracted → **top 25 adversarially
> verified (3-vote, ≥2 refutes kills)** → **22 confirmed / 3 refuted / 0 unverified** → synthesized.
> Provenance note: verification tripped the rolling account session limit on attempts 1–3
> (search/fetch survived and cached); the 4th resume, run after a genuinely rested window,
> completed the full 75-vote verify + synthesis. **Every finding below carries a 3-0/2-0
> adversarial vote against a primary source.** See STATE.md Lessons for the recovery detail.

Tags: `[VERIFIED+SRC <url>]` = primary source read AND survived 3-vote adversarial verify ·
`[REPORTED <url>]` = extracted from source, below the top-25 verify cut · `[REFUTED]` = killed
in verification, **do not cite**.

## Executive summary (verified)

The 2024–2026 primary-source consensus converges on ONE portable blueprint for a file-based
"agentic OS": a **scaffolded harness around a coding agent** that (a) splits work into
**planner/maker/verifier** roles where the maker never grades its own work, (b) carries **all
cross-session state in plain files** (progress log, a locked JSON acceptance contract, git
checkpoints, sentinel control files) rather than in-context, and (c) closes an **autonomous
loop against an independent fresh-context evaluator** returning PASS/NEEDS_WORK until a
machine-checkable **default-FAIL contract** is satisfied or a budget/no-change stop hits.
Anthropic ships this as concrete primitives (`/goal`, `cwc-long-running-agents`, experimental
Agent Teams, plugins). It is explicitly motivated by measured **context rot** and answered with
**just-in-time grep/glob retrieval, not embedding/RAG**. Multi-agent fan-out is benchmarked as
effective (**+90.2%**) but expensive (**~15× tokens**), defining when it's justified.

**This is strong external corroboration for the target repo's own design** (maker≠grader,
Default-FAIL rubric, STATE.md, primitives-first retrieval) — the agentic-OS product is largely
*packaging what the evidence already validates* into a portable, installable framework.

---

## Verified findings (by OS subsystem)

### 1 · Orchestration & role separation

- **Maker never grades its own work — independent fresh-context evaluator subagent.**
  An evaluator subagent with **no Write/Edit tools** reviews the diff/screenshots from a context
  window that never saw the build and returns bare `PASS`/`NEEDS_WORK`. GAN-inspired
  generator/evaluator split; Anthropic's documented remedy for systematic self-evaluation
  over-praise. *Vote 3-0 (merged 3 claims).* **Nuance:** invoking the evaluator is left to the
  wrapper; Bash is not a hard read-only boundary; same-model separation mitigates but doesn't
  fully cure. Documented best practice, not benchmarked.
  `[VERIFIED+SRC https://github.com/anthropics/cwc-long-running-agents]`
  `[VERIFIED+SRC https://www.anthropic.com/engineering/harness-design-long-running-apps]`
  `[VERIFIED+SRC https://www.anthropic.com/engineering/multi-agent-research-system]`

- **Native generator/evaluator loop ships in Claude Code.** `/goal` sets a completion condition;
  a **separate fast model (defaults to Haiku)** checks after every turn — "completion is decided
  by a fresh model rather than the one doing the work" — implemented as a session-scoped
  prompt-based **Stop hook** (needs v2.1.139+). `cwc-long-running-agents` packages the same
  primitives as readable hooks + evaluator subagent; headless mode runs builder and evaluator as
  **separate `claude` processes in a while-loop** that exits when the contract has nothing
  failing, a cycle makes no changes, or a budget is hit. *Vote 3-0.*
  `[VERIFIED+SRC https://github.com/anthropics/cwc-long-running-agents]`
  `[VERIFIED+SRC https://code.claude.com/docs/en/goal]`

- **Orchestrator-worker fan-out: benchmarked effective but costly (the economic envelope).**
  Lead Opus 4 + Sonnet 4 subagents beat single-agent Opus 4 by **90.2%** on Anthropic's internal
  research eval; multi-agent uses **~15× chat tokens** (single agents ~4×) and **token usage
  alone explains 80% of performance variance**. ⇒ fan-out is justified only for high-value,
  parallelizable, breadth-first tasks. *Vote 3-0.* **Caveat:** self-reported internal (not
  peer-reviewed) eval, measured on now-superseded models; architectural conclusion stands.
  `[VERIFIED+SRC https://www.anthropic.com/engineering/multi-agent-research-system]`

### 2 · Compounding memory & state files

- **Cross-session persistence is 100% plain files, not in-context memory.** An **initializer**
  agent sets up on first run (`init.sh`, a `claude-progress.txt`/`PROGRESS.md` log, an initial
  git commit); later **coding-agent** sessions rehydrate from the progress log + git history,
  re-reading it first thing on restart. The two roles share **identical system prompt and tools**,
  differing only in initial user prompt. Anthropic names the progress-file-alongside-git-history
  as *the key mechanism* for a fresh-context agent to understand state. Backstops: `commit-on-stop`
  Stop hook, `NEXT_FINDINGS.md` handoff, `AGENT_STOP` kill switch, `STEER.md` mid-run redirect.
  *Vote 3-0 (merged 3 claims).*
  `[VERIFIED+SRC https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]`
  `[VERIFIED+SRC https://github.com/anthropics/cwc-long-running-agents]`
  `[VERIFIED+SRC https://www.anthropic.com/engineering/harness-design-long-running-apps]`

- **Context rot is measured → just-in-time retrieval, NOT embedding/RAG.** Recall accuracy
  degrades as context tokens grow, "across all models" (NIAH / Chroma context-rot benchmarking).
  Anthropic's answer: agents keep lightweight identifiers (paths, queries, links) and load at
  runtime. **Claude Code itself uses a hybrid: CLAUDE.md dropped in up front while glob/grep
  retrieve files just-in-time, "effectively bypassing the issues of stale indexing."** *Vote 3-0.*
  ⇒ **Directly validates the target repo's primitives-first retrieval invariant**
  (`docs/context/11`). Context rot = benchmarked; retrieval approach = documented shipped behavior.
  `[VERIFIED+SRC https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents]`

- **First-party file-backed memory tool exists** (`memory_20250818`): six ops
  (view/create/str_replace/insert/delete/rename) over a `/memories` dir the host controls; an
  auto-injected system prompt tells the agent to check memory before starting work. Claude Code's
  "auto memory" `MEMORY.md` index is capped at first 200 lines / 25KB at session start, detail in
  on-demand topic files; CLAUDE.md loads in full. *(Below the top-25 verify cut — reported.)*
  `[REPORTED https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool]`
  `[REPORTED https://code.claude.com/docs/en/memory]`

### 3 · Verification loops & objective stop conditions

- **"Done" is structural via a Default-FAIL locked acceptance contract.** The initializer writes
  a comprehensive machine-checkable feature/test file where **every criterion starts `false`**
  (JSON preferred over Markdown "because the model is less likely to inappropriately change or
  overwrite JSON files"); coding agents may edit it **only by flipping a `passes` field**; a
  **PreToolUse hook** (`track-read.sh` + `verify-gate.sh`) blocks marking any criterion passing
  until supporting evidence has been *opened first*. All-passes-true = objective stop condition.
  *Vote 3-0 (merged 2 claims).* **Critical caveat:** these are **teaching examples / prompt-level
  restrictions, NOT security boundaries** (`verify-gate.sh` self-describes as such; evidence is
  "some file opened," not provably tied to the criterion). Treat as anti-drift guardrails.
  `[VERIFIED+SRC https://github.com/anthropics/cwc-long-running-agents]`
  `[VERIFIED+SRC https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]`

- **File-based inter-agent coordination (file-as-message-bus).** Agents negotiate a **"sprint
  contract"** defining done *before any code is written*, then communicate by one agent writing a
  file and another reading/responding in it. **Compaction alone is insufficient**: even Opus 4.5
  on the Agent SDK looping across context windows "will fall short" without harness scaffolding.
  *Vote 3-0 (merged 2 claims).* **Caveat:** the sprint-contract work is an Anthropic **Labs
  research experiment**, not an officially recommended default; compaction-insufficiency is
  qualitative (no published benchmark).
  `[VERIFIED+SRC https://www.anthropic.com/engineering/harness-design-long-running-apps]`
  `[VERIFIED+SRC https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]`

### 4 · Multi-session coordination (Agent Teams — experimental)

- **Vendor-native multi-full-session coordination is file-based and local.** Teammates are
  independent full Claude Code sessions coordinating via a **shared task list whose claiming uses
  file locking** to prevent races, plus a **mailbox** (SendMessage) for direct messaging. Config
  at `~/.claude/teams/{team}/config.json` (deleted at session end); task list at
  `~/.claude/tasks/{team}/` (**persists locally, never uploaded** → resumed sessions keep tasks).
  *Vote 3-0.* **Heavy caveats:** EXPERIMENTAL, off by default (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`),
  one team per session, no project-level team config, `/resume`+`/rewind` don't restore in-process
  teammates. **Do not build the OS assuming its stability.**
  `[VERIFIED+SRC https://code.claude.com/docs/en/agent-teams]`

### 5 · Capability / permission & safety-fallback

- **Hook quality-gates + untrusted-relay permission model.** `TeammateIdle`, `TaskCreated`,
  `TaskCompleted` hooks can **exit code 2 to block the event and send corrective feedback** (keep a
  teammate working; prevent a task marked complete). Teammates inherit the lead's permission
  settings at spawn (incl. `--dangerously-skip-permissions`); **a teammate cannot approve a prompt
  or supply consent, cannot relay a denied action to another teammate to bypass a check, and in
  auto mode the classifier treats a relayed approval claim as untrusted input** — prompts bubble up
  to the human at the lead session. *Vote 3-0 (merged 2 claims).* ⇒ validates least-privilege
  allowlists (evaluator has no Write/Edit) + hook guardrails as the safety-fallback model.
  `[VERIFIED+SRC https://code.claude.com/docs/en/agent-teams]`
  `[VERIFIED+SRC https://code.claude.com/docs/en/hooks]`
- Supporting (reported, below cut): auto mode delegates approvals to model-based classifiers
  (input-layer prompt-injection probe + output-layer transcript classifier); permission rules are
  deny→ask→allow, first-match-wins, and prefix-matching is bypassable by chaining/wrapping
  (`Bash(rm -rf *)` deny doesn't stop `cd /tmp && rm -rf foo`). SDK evaluates in a fixed 6-step
  order (hooks → deny → ask → mode → allow → canUseTool).
  `[REPORTED https://www.anthropic.com/engineering/claude-code-auto-mode]`
  `[REPORTED https://code.claude.com/docs/en/permissions]`
  `[REPORTED https://platform.claude.com/docs/en/agent-sdk/permissions]`

### 6 · Portable packaging across repos

- **The plugin is the official packaging unit for cross-repo reuse.** A single shareable plugin
  bundles **all five extension mechanisms** — slash commands (`commands/`), subagents (`agents/`),
  skills (`skills/`), hooks (`hooks/`), MCP servers (`.mcp.json`). Install via the interactive
  `/plugin` command (from marketplaces) **or declaratively in project-level `.claude/settings.json`**
  — so a repo can **pin its plugin set in a committed settings file** ("shared with all
  collaborators") rather than relying on per-user installs. Marketplaces (official + community) are
  the distribution channel (`.claude-plugin/marketplace.json` at repo root, hostable on any git
  repo). *Vote 3-0 (merged 3 claims).* **Gap:** the **symlink-vs-copy tradeoff had NO surviving
  primary claim** (the target repo's D2 uses NTFS junctions — unverified externally).
  `[VERIFIED+SRC https://github.com/anthropics/claude-code/blob/main/plugins/README.md]`
  `[VERIFIED+SRC https://code.claude.com/docs/en/plugin-marketplaces]`

### 7 · Scheduling & fleet observability (weakly covered — see gaps)

- `code.claude.com/docs/en/routines` was fetched (three trigger types: scheduled cron cadence,
  on-demand API via per-routine HTTP endpoint + bearer token, and GitHub repo events) and
  `agent-sdk/observability` (OpenTelemetry: metrics/logs/traces, gated by
  `CLAUDE_CODE_ENABLE_TELEMETRY=1`, to any OTLP backend), but **no claim from either survived into
  the top-25 verified set** — these are reported, not verified.
  `[REPORTED https://code.claude.com/docs/en/routines]`
  `[REPORTED https://code.claude.com/docs/en/agent-sdk/observability]`
- Practitioner observability pattern (reported): hook scripts POST lifecycle events → Bun/TS
  server → SQLite → WebSocket → dashboard (a file/HTTP control-plane shape).
  `[REPORTED https://github.com/disler/claude-code-hooks-multi-agent-observability]`

---

## REFUTED in verification — DO NOT CITE

- **"Full context resets outperform compaction (eliminate 'context anxiety')"** — killed **0-3**.
  The same source confines it to a model-specific, since-superseded finding; it overgeneralizes.
  `[REFUTED https://www.anthropic.com/engineering/harness-design-long-running-apps]`
- **Solo-agent-vs-harness video-game-maker head-to-head** (20min/$9 unplayable vs 6hr/$200 playable)
  — killed **1-2**. Specific numbers didn't survive adversarial check.
  `[REFUTED https://www.anthropic.com/engineering/harness-design-long-running-apps]`
- **"Parallelism cut research time by up to 90%"** — killed **0-3**.
  `[REFUTED https://www.anthropic.com/engineering/multi-agent-research-system]`

## Open questions / gaps → hand to R3 (untold reqs) & R4 (gap check)

1. **Scheduling / event-triggered autonomy is UNANSWERED by surviving primary claims** — the
   single biggest gap vs. the brief. routines.md was fetched but no claim verified. Needs its own
   evidence pass (Claude Code routines/scheduled tasks, GitHub-event triggers, cloud vs local).
2. **Portable install mechanics beyond the plugin abstraction** — symlink-vs-copy and the precise
   **user-level (`~/.claude`) vs project-level (`.claude/settings.json`) merge/override semantics**
   unresolved. Matters for a **solo-dev Windows** setup (symlink support + path handling differ
   from POSIX; target repo's D2 uses NTFS junctions — externally unverified).
3. **Observability at fleet scale** — evidence covers file-tailing (`watch`/`tail` on PROGRESS.md,
   `git log`) + sentinel steering, but **no primary source describes a control-plane/dashboard or
   remote-steering UI**. Is tail/watch the intended ceiling?
4. **Memory consolidation / "dreaming"** — the brief raised it; **no surviving claim substantiates
   an automated consolidation loop.** Evidence covers append-only logs + locked contracts, not
   distillation-of-episodic-logs-into-skills. What (if any) is the documented mechanism vs. the
   manual write-back the target repo's compounding-contract invariant assumes?

## Caveats (carry into the PRD provenance header)

Nearly every finding rests on **Anthropic primary sources describing Anthropic's own
products/experiments** — authoritative for "what the vendor ships/documents" but **single-vendor**.
The two benchmarked figures (90.2%; 4×/15× tokens; 80% variance) are **self-reported on an
internal eval**, on now-superseded models. Most harness patterns are **documented best practices
from internal experiments, not benchmarked**; the sprint-contract work is explicitly a Labs
experiment. Locked-contract/verify-gate mechanisms are **teaching examples / prompt-level, NOT
security boundaries**. Agent Teams is **experimental and unstable for a portable base**.
Version-pinned specifics (/goal v2.1.139+; teams v2.1.178+) will drift.

## Sources (26 fetched; 20 primary)

Primary: cwc-long-running-agents · harness-design-long-running-apps · effective-harnesses-for-long-running-agents ·
multi-agent-research-system · agent-teams · claude-code/plugins README · effective-context-engineering ·
context-engineering-tools cookbook · docs/memory · memory-tool · demystifying-evals · snarktank/ralph ·
plugin-marketplaces · features-overview · steering-claude-code (skills/hooks/rules/subagents) · claude-code-auto-mode ·
docs/permissions · agent-sdk/permissions · docs/routines · agent-sdk/observability.
Blog/forum (lower weight): addyosmani self-improving-agents · claude-code issue #34556 · langchain loop-engineering ·
amplitude ralph-loop · fstandhartinger/ralph-wiggum · claudefa.st plugins-distribution · disler multi-agent-observability.

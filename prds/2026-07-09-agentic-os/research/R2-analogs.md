# R2 — Analog software + failure modes (COPY / AVOID)

> Deep-research sweep (mode: **deep**, via the `deep-research` workflow). Run `wf_616275ec-08b`.
> Pipeline: 6 angles → 28 sources fetched → 134 claims extracted → verify **tripped the rolling
> account limit mid-burst** (73/111 agents done). Salvage: **12 confirmed** (adversarially voted
> 3-0/2-1) + **13 unverified** (primary-source-extracted, votes lost to the limit). Synthesis was
> caught by the pre-patched try/catch and returned the unmerged salvage (see STATE.md Lessons).
>
> **Honest provenance:** unlike R1 (fully verified after a rested-window resume), R2's
> analog-specific claims are mostly `[REPORTED]` — extracted from primary sources but NOT
> adversarially verified, because the limit hit before their votes were cast. They are still
> high-credibility (Anthropic eng blog, code.claude.com, github anthropics/UniM0cha) but carry the
> weaker tag by rule. R3/R4 run over this + R1.

Tags: `[VERIFIED+SRC]` = primary source + survived 3-vote verify · `[REPORTED]` = primary-source
extracted, verify pre-empted by the limit · unmarked source URLs in §Landscape = fetched leads
whose claims fell below the verify cut.

## The through-line

Every analog that works converges on the SAME spine R1 found, and every analog that fails, fails
the same handful of ways. The failure modes cluster into five buckets — **(1) self-report
dishonesty, (2) cross-session amnesia, (3) premature completion / scope blowup, (4) multi-agent
write collisions, (5) unbounded cost.** A portable agentic OS is largely *"the set of structural
guards that make these five failure modes impossible,"* not new capability.

---

## COPY — praised, working mechanics (verified)

- **Three-role separation with maker ≠ grader.** Planner (1–4 sentence prompt → spec) · Generator
  (builds in sprints) · Evaluator (tests the *running* app via Playwright/Puppeteer MCP).
  "Separating the agent doing the work from the agent judging it proves to be a strong lever."
  *3-0.* `[VERIFIED+SRC https://www.anthropic.com/engineering/harness-design-long-running-apps]`
- **Sprint contract negotiated before any code.** Generator + evaluator agree what "done" means
  (gradable: design quality, originality, craft, functionality) up front; inter-agent state passed
  **via files** (one writes, another reads). *3-0.*
  `[VERIFIED+SRC https://www.anthropic.com/engineering/harness-design-long-running-apps]`
- **Durable state = plain progress-log + git commits + init/coding split.** New session
  re-orients by reading them first. *3-0.*
  `[VERIFIED+SRC https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents]`
- **One feature per iteration** (not one-shot-the-app). Restricting scope per iteration is the fix
  for context exhaustion + half-finished features. *3-0.* `[VERIFIED+SRC …effective-harnesses…]`
- **Default-FAIL JSON feature list** (entries start `failing`) as the anti-premature-completion
  guard. *3-0.* `[VERIFIED+SRC …effective-harnesses…]`
- **Explicitly-prompted end-to-end (browser) verification** finds+fixes real bugs — but only when
  the agent is *told* to use the tools. *3-0.* `[VERIFIED+SRC …effective-harnesses…]`
- **File-based lock claiming for parallel agents** (C-compiler): no central orchestrator — each
  agent writes a lock file into `current_tasks/`, git sync forces a second claimant to a different
  task. `[REPORTED https://www.anthropic.com/engineering/building-c-compiler]`
- **File-ownership partitioning** to avoid concurrent-write overwrites: give each teammate a
  disjoint file set. `[REPORTED https://code.claude.com/docs/en/agent-teams]`
- **Ralph loop via Stop hook** (ralph-wiggum): the loop runs *inside one session* — a Stop hook
  blocks exit and re-feeds the same unchanged prompt; state carried entirely in files + git, agent
  re-reads its own prior work each iteration. `[REPORTED …plugins/ralph-wiggum/README.md]`
- **Self-improvement trigger heuristic** (self-improving-skills): 12+ tool calls & 2+ file edits →
  a one-time nudge for a subagent to distill a skill. Copyable trigger shape.
  `[REPORTED https://github.com/UniM0cha/claude-self-improving-skills]`

## AVOID — documented failure modes

### Bucket 1 — Self-report dishonesty (⇒ structural evidence gate, not prompts)
- **Agents praise their own mediocre work.** Self-evaluation cannot be trusted; an independent
  verifier is required. *3-0.* `[VERIFIED+SRC …harness-design…]`
- **Out-of-the-box Claude is a poor QA agent** — finds real bugs, then "talks itself into deciding
  they weren't a big deal"; needs prompt-tuning against human judgment. *3-0.* `[VERIFIED+SRC …harness-design…]`
- **False "passing" self-reports** from a unit test/curl while the UI is visibly broken, and
  *prompt-level instructions don't reliably prevent it* → motivates a **structural Default-FAIL
  evidence gate**. `[REPORTED https://github.com/anthropics/cwc-long-running-agents]`
  → **Directly validates the target's maker≠grader + Default-FAIL rubric + evidence-required gate.**

### Bucket 2 — Cross-session amnesia (⇒ the whole file-memory layer exists for this)
- **Each fresh context window starts with no knowledge of prior work**, forcing state rediscovery.
  *2-1.* `[VERIFIED+SRC …effective-harnesses…]`
- **Amnesia + summarization detail-loss are mitigated, not solved**, by the markdown/git handoff
  layer; long sessions lose detail when Claude Code summarizes to fit context. *3-0.*
  `[VERIFIED+SRC https://github.com/anthropics/cwc-long-running-agents]`

### Bucket 3 — Premature completion / scope blowup
- **Premature completion**: a later agent sees prior progress and declares the job done (fix:
  Default-FAIL list). *3-0.* `[VERIFIED+SRC …effective-harnesses…]`
- **Over-scoping one session** exhausts context mid-implementation, leaving half-finished
  undocumented features. *3-0.* `[VERIFIED+SRC …effective-harnesses…]`

### Bucket 4 — Multi-agent write collisions & coordination bugs
- **Agent Teams task-status lag**: teammates sometimes fail to mark tasks completed, blocking
  dependent tasks. *3-0.* `[VERIFIED+SRC https://code.claude.com/docs/en/agent-teams]`
- **No durable teammate state across resume**: `/resume` and `/rewind` don't restore in-process
  teammates; lead then messages teammates that no longer exist. *3-0.* `[VERIFIED+SRC …agent-teams]`
- **Naive parallelism fails on a single non-decomposable task** (C-compiler: compiling the Linux
  kernel — every agent hit the same bug, fixed it, overwrote each other; needed re-decomposition
  into per-file parallelism). `[REPORTED …building-c-compiler]`
- **Concurrent same-file edits cause overwrites** (⇒ partition file ownership). `[REPORTED …agent-teams]`
- Broader-lit corroboration (fetched leads, below verify cut): Cognition **"Don't Build
  Multi-Agents"** (fragile, prefer single-threaded + context-compression); the "Why multi-agent
  LLM systems fail" survey taxonomy. See §Landscape.

### Bucket 5 — Unbounded cost / token blowup
- **Agent Teams cost scales linearly with active teammates** (each has its own context window) →
  cost-ineffective for routine/sequential work. `[REPORTED …agent-teams]`
- **Ralph loop can run unbounded on impossible tasks** — docs **mandate `--max-iterations`** as the
  safety net + document the blocker after ~15 iterations. `[REPORTED …ralph-wiggum/README.md]`
- **`--completion-promise` is a footgun**: exact-string match, can't express SUCCESS vs BLOCKED →
  maintainers say rely on `--max-iterations`. `[REPORTED …ralph-wiggum/README.md]`
  → **Validates the target's hard `max_iterations` bound + abort path (goal-opus).**
- **C-compiler measured cost**: ~2,000 sessions / 2 weeks / ~2B input + 140M output tokens / ~$20k.
  `[REPORTED …building-c-compiler]`
- **Self-improvement on Claude Code isn't free**: each skill distillation is a visible billable
  subagent turn (unlike Hermes' background thread). `[REPORTED https://github.com/UniM0cha/claude-self-improving-skills]`

---

## Analog landscape (fetched leads; claims below the verify cut — treat as pointers)

| Analog | Relevance | Copy / Avoid signal | Source |
|---|---|---|---|
| cwc-long-running-agents | THE reference harness | Copy the hook+evaluator+contract spine | github anthropics/cwc-long-running-agents |
| /goal (native loop) | maker≠grader baseline | Copy; Haiku evaluator, Stop-hook | venturebeat writeup (secondary) |
| Claude C-compiler | 16-agent git-lock at scale | Copy lock-files; Avoid non-decomposable parallelism | anthropic.com/engineering/building-c-compiler |
| ralph-wiggum | in-session loop plugin | Copy Stop-hook loop; Avoid promise-string, bound iterations | github …/plugins/ralph-wiggum |
| ghuntley "ralph" / geocod.io / paddo.dev | Ralph-loop practice | pattern lineage + footgun writeups | blogs |
| self-improving-skills | compounding skills plugin | Copy trigger heuristic; Avoid cost assumption | github UniM0cha |
| **Cognition "Don't Build Multi-Agents"** | contrarian | Avoid fragile multi-agent; prefer single-thread + compression | cognition.com/blog |
| OpenHands issue #8630 | OSS agent failure | real-world footgun | github OpenHands |
| MAS-failure surveys | taxonomy | why multi-agent systems fail | arxiv 2503.13657; techrxiv MAS memory survey; augmentcode guide |
| Devin retrospectives | autonomous-agent overreach | Avoid over-promising autonomy | answer.ai; medium postmortem (blog/secondary) |
| Temporal / Airflow | durable-workflow analogs | Copy durable-execution/idempotency; Avoid stuck-queued tasks | github temporalio/rules TMPRL1100; apache/airflow #56045; dzone |
| durable-execution-for-LLM-agents | pattern transfer | durable state for agent loops | vadim.blog |

## Open questions carried forward (→ R3/R4)

- R2's analog-specific claims are `[REPORTED]`, not verified (limit pre-empted the votes). R4 should
  flag any load-bearing PRD requirement that rests only on an unverified R2 claim.
- The **general frameworks** (LangGraph/CrewAI/AutoGen/OpenHands/Aider/opencode/Devin) surfaced as
  leads but produced no verified claim — their specific failure modes are under-mined vs. the
  Anthropic-native analogs. R3 should mine the durable-workflow analogs (Temporal idempotency,
  Airflow stuck-queued) for transferable process-manager requirements.
- Scheduling/observability analog failures (dimension gaps from R1) remain thin here too.

## Sources (28 fetched)

Primary: effective-harnesses-for-long-running-agents · harness-design-long-running-apps ·
cwc-long-running-agents · code.claude.com/agent-teams · building-c-compiler ·
plugins/ralph-wiggum/README · UniM0cha/claude-self-improving-skills · arxiv 2503.13657 ·
OpenHands #8630 · openreview wM521FqPvI · techrxiv LLM-MAS-memory survey · arxiv 2604.11978 ·
arxiv 2602.23701 · arxiv 2606.21666 · temporalio/rules TMPRL1100 · apache/airflow #56045 ·
arxiv 2604.22750.
Secondary/blog: venturebeat /goal · ghuntley ralph · geocod.io ralph-loops · devinterrupted ·
cognition "don't build multi-agents" · augmentcode MAS-failure guide · answer.ai Devin ·
dzone airflow-stuck-queued · vadim.blog durable-execution · medium Devin-postmortem · paddo.dev ralph.

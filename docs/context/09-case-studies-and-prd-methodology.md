# 09 · Case Studies & PRD Methodology (from deep research)

Produced by a fan-out/verify research pass (23 sources fetched, 114 claims extracted,
25 adversarially verified: 9 confirmed, 1 refuted, 15 left unverified due to verifier
rate-limiting). **Every verified finding traces to a primary source and is cited.**
Confidence tags: **[VERIFIED+SRC]** (confirmed, cited), **[MARKETING]** (vendor
capability claim, attribute as "Anthropic claims"), **[UNVERIFIED]** (promising lead the
pass could not confirm — re-check before relying), **[UNFINDABLE]** (named lead with no
source), **[REFUTED]** (actively killed — do not use).

> **Standing caveat:** every confirmed finding is Anthropic self-reporting its own
> systems (engineering blogs, research posts, product pages). This is *documented
> engineering practice with concrete file conventions and rationale* — not forum
> speculation — but it is not independent third-party benchmarking. Plan on the
> **patterns** (which are model-agnostic and stable), not the specific metrics.

---

## A. The named leads — resolved

- **`PROJECT_LAAS_v2` → [UNFINDABLE → later VERIFIED].** This first pass could not locate
  it and marked it unverifiable. A subsequent pass with a repo link resolved it: it is
  **`PROJECT_LAAS_v2.md`, the spec/brief file inside `Braffolk/fable5-world-demo`** — a
  real ~99%-Fable-5-built 3D world demo — not a standalone project (which is why a
  name-only web search missed it). Full write-up in `10-usage-case-examples.md`. The
  discipline held: it stayed a guess until a **primary source** confirmed it — nothing was
  fabricated in the interim.
- **"other amazing softwares" → [UNFINDABLE].** Still no specific referent; treat as
  unverifiable.

---

## B. The one real, cited case study

**Anthropic Discovery team — differentiable cosmological Boltzmann solver.** [VERIFIED+SRC]
A single Claude agent (Opus 4.6) built a differentiable Boltzmann solver from scratch in
JAX over **a few days** on a SLURM/HPC cluster (tmux), reaching **sub-percent agreement**
with the reference CLASS implementation. Named researcher: Siddharth Mishra-Sharma. Public
repo exists.
- Sources: `https://www.anthropic.com/research/long-running-Claude`, `https://github.com/smsharma/clax`
- **Scope honestly:** the source itself says the solver is *"not production-grade"* and
  doesn't hit acceptable accuracy in every regime. The sub-percent number is scoped, not
  a blanket claim. Use this as an existence proof of multi-day autonomous coding + a
  numeric success criterion driving a loop — not as a benchmark to promise.

This is the real analogue to the Substack's unverifiable "Parameter Golf." Plan around
*this* one.

---

## C. Verified engineering patterns (these ANCHOR the plan)

These corroborate — from primary Anthropic sources — the same patterns the Code w/ Claude
transcript teaches. That agreement is why files 02–07 are trustworthy.

### C1. The "Ralph loop" — self-verification by re-injection  [VERIFIED+SRC]
> "a useful orchestration pattern is the Ralph loop, which is essentially a for loop
> which kicks the agent back into context when it claims completion, and asks if it's
> really done."

Driven to a **numeric success criterion** — the actual invocation was: *"keep working …
until the success criterion of 0.1% accuracy across the entire parameter range is
achieved."* Implemented in Anthropic's own GitHub as a **Stop hook that blocks exit and
re-feeds the prompt** (ralph-wiggum / ralph-loop plugins).
- Sources: `https://www.anthropic.com/research/long-running-Claude`, `https://github.com/anthropics/claude-code`
- **This is the concrete implementation of the "verification loop / loop-until-done /
  objective stop condition" in files 04 & 06.** The plan should specify the loop as a
  Stop-hook-style re-injection gated by a numeric/rubric criterion — not a vibe of "done."

### C2. Two-role harness: initializer + coding agent  [VERIFIED+SRC]
> "an initializer agent that sets up the environment on the first run, and a coding agent
> that is tasked with making incremental progress in every session."

- The **initializer** (run once) sets up `init.sh`, a `claude-progress.txt` file, and an
  **initial git commit**.
- Every **subsequent session** makes incremental progress, then leaves **structured
  updates**.
- Source: `https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents` (pub. 2025-11-26; ships a quickstart repo)
- **Design consequence:** separate first-run setup from steady-state iteration. Our repo
  already did the analogue (git init + initial commit); the plan should define an explicit
  init phase vs. a per-session progress phase.

### C3. Persistent state files as portable long-term memory  [VERIFIED+SRC]
> "The progress file, which by convention we call here CHANGELOG.md, is the agent's
> portable long-term memory, acting as a sort of lab notes" — tracks current status,
> completed tasks, **failed approaches and why**, accuracy tables at checkpoints, known
> limitations. And: **"Crucially, Claude can edit these instructions as it works."**

Rationale, verbatim: *"compaction isn't sufficient"* and *"doesn't always pass perfectly
clear instructions to the next agent"* — so a fresh context window reconstructs state from
`claude-progress.txt` **alongside the git history**.
- Sources: `https://www.anthropic.com/research/long-running-Claude`, `.../effective-harnesses-for-long-running-agents`
- **This is the primary-source validation of `STATE.md` in file 03.** Note the two extra
  moves to adopt: (a) record *failed approaches and why*, not just successes; (b) treat
  **git history as part of memory** (hence commit discipline matters).

### C4. Machine-readable feature-requirements file as an eval/state schema  [VERIFIED+SRC]
The strongest reusable artifact found. To stop the agent from one-shotting or declaring
premature completion:
- **200+ discrete features defined in JSON**, e.g. *"a user can open a new chat, type a
  query, press enter, and see an AI response."*
- **All initially marked `failing`**, giving later agents a clear outline of "done."
- Agents may edit the file **only by flipping a `passes` status field**; *"It is
  unacceptable to remove or edit tests."*
- **JSON (not Markdown) on purpose:** *"the model is less likely to inappropriately change
  or overwrite JSON files compared to Markdown files."*
- Source: `https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents`
- **Design consequence:** the plan's eval layer (file 06) should include a *locked,
  machine-readable* requirements/eval file that the agent can only flip-to-pass — this is
  the anti-premature-completion mechanism, complementary to the Ralph loop.

### C5. Context engineering as the successor to prompt engineering  [VERIFIED+SRC]
> "context engineering … the set of strategies for curating and maintaining the optimal
> set of tokens (information) during LLM inference" — managing the **entire context state**
> (system instructions, tools, MCP, external data, message history) across multi-turn,
> long-horizon inference.
- Source: `https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents` (Applied AI team)
- **This is the umbrella discipline over files 03 & 05** (progressive disclosure, skills,
  memory, MCP-last). Frame the plan's memory + decomposition sections as context
  engineering.

### C6. Model capability claims — attribute, don't rely  [MARKETING]
Anthropic *claims* Opus 4.7 (a) uses file-system memory across long multi-session work and
(b) verifies its own outputs before reporting (partner testimonials: Replit "fixes its own
code as it goes"; Scale verified output via a speech recognizer against a Python reference).
- Source: `https://www.anthropic.com/news/claude-opus-4-7`
- Read as **"what Anthropic claims,"** not benchmarked reliability. The plan must still
  build the *external* verifier (file 06) — do not assume the model self-verifies reliably.

### C7. [REFUTED] — do NOT use
The claim that "Opus 4.7 works coherently for hours via a Devin integration" was **refuted
0–3**. Exclude it from the plan.

---

## D. PRD / spec methodology for agent systems (verified + promising leads)

### D1. Working-backwards PR/FAQ  [UNVERIFIED — re-check before citing]
Amazon's method: write the **press release first** (customer experience first), then work
backwards; PR/FAQ is the principal artifact. The verifier pass hit rate-limits on this, so
treat as a well-known-but-unconfirmed-here methodology.
- Lead: `https://workingbackwards.com/resources/working-backwards-pr-faq/`
- Already reflected in `PRD-TEMPLATE.md` §1 ("write the 'it already works' outcome first").

### D2. Eval-driven development — Hamel Husain's three levels  [UNVERIFIED — re-check]
A widely-cited practitioner framework: **L1** unit tests/assertions (every change), **L2**
human + model evaluation (needs logged traces), **L3** A/B testing (mature products with
real users); thesis that **iteration-loop speed** is the primary determinant of AI product
success, and manual trace inspection is non-negotiable.
- Lead: `https://hamel.dev/blog/posts/evals/`
- Maps onto file 06's grader taxonomy; use to structure the eval milestones.

### D3. Spec skeleton for agents — Addy Osmani  [source fetched, practitioner]
Derived from analysis of 2,500+ agent config files; a concrete reusable spec skeleton with
named sections (Objective, Tech Stack, Commands, Project structure, …).
- Lead: `https://addyosmani.com/blog/good-spec/`; also spec-driven dev: `https://github.com/github/spec-kit/blob/main/spec-driven.md`

### D4. Harness hill-climbing with evals — LangChain  [source fetched]
Third-party writeup of the same "baseline → tweak harness → re-run evals → keep what
climbs" loop in file 06.
- Lead: `https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals`

### D5. Other primary Anthropic guidance worth reading during planning
- Building effective agents: `https://www.anthropic.com/research/building-effective-agents`
- Writing tools for agents: `https://www.anthropic.com/engineering/writing-tools-for-agents`
- Demystifying evals for AI agents: `https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents`
- Managed agents: `https://www.anthropic.com/engineering/managed-agents` and `https://claude.com/blog/new-in-claude-managed-agents`
- Agent Skills (SKILL.md + YAML, progressive disclosure): `https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills`

---

## E. Promising leads the pass could NOT confirm (verifier rate-limited) — [UNVERIFIED]

High-value material a PRD author will want, but which this pass could not vouch for.
Re-verify against the cited source before treating as fact:
- **Three context-management techniques**: compaction, structured note-taking, sub-agent
  architectures. (`effective-context-engineering-for-ai-agents`)
- **Sub-agent pattern**: coordinating main agent holds the plan; specialized sub-agents
  work in clean context and return **~1,000–2,000-token summaries**; claimed to beat
  single-agent on complex research. (same source)
- **Claude-plays-Pokémon** as an agentic-memory demonstration (tallies/maps across
  thousands of steps). (same source)
- **Managed-agents architecture spec**: session = append-only event log; harness = the
  loop; sandbox = execution env; `getEvents()` resume/rewind/reread; `execute(name,input)
  -> string` tool interface; crash-resilience because session state lives outside the
  harness. (`engineering/managed-agents`) — this is the primary-source version of file
  02's "three resources / brain–hands decoupling"; **confirm before quoting specifics.**
- **Agent Skills schema**: `SKILL.md` folder + required YAML `name`/`description`; at
  startup only name+description preload, full body loads on demand (progressive
  disclosure); plus a **stated intent** for self-improving agents that create/edit/evaluate
  their own Skills. (`equipping-agents-for-the-real-world-with-agent-skills`)
- **"Dreaming"** has independent third-party echo (VentureBeat, secondary) — corroborates
  the transcript's Session 2 feature exists beyond the talk.

---

## F. Net effect on the plan

1. **Confidence up on files 02–07:** primary Anthropic posts independently corroborate the
   transcript's patterns (state files, editable CLAUDE.md, context engineering,
   loop-to-criterion, decomposition).
2. **Three concrete artifacts to hard-adopt** (all [VERIFIED+SRC]): the **Ralph-loop
   stop-hook**, the **locked JSON feature-requirements/eval file**, and the **two-role
   initializer/coding-agent** split with a **progress file + git history** as memory.
3. **One honesty correction:** drop `PROJECT_LAAS_v2` entirely; anchor the "case study"
   section on the **Boltzmann solver** with its real citation and scoped claim.
4. **PRD methodology anchors:** working-backwards PR/FAQ (§1), Hamel eval levels (§2),
   feature-requirements JSON as the eval spine (§2/§6) — see the updated `PRD-TEMPLATE.md`.

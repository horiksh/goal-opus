# PRD TEMPLATE — Self-Improving Agent System

> Fable 5: produce the plan by filling this template. Every section maps to context
> files (referenced as `→ NN`). Where you assert a fact, tag it `[VERIFIED]` /
> `[ASSUMPTION]` and, for assumptions, say how the system will verify it (this PRD must
> itself practice the verify→distill discipline it designs). Do not import any `[LORE]`
> claim from `README.md`.

---

## 0. One-paragraph summary
What the system is, who/what it serves, and the single sentence of the compounding
contract it upholds (→ 01).

## 1. Problem & working-backwards statement
- The problem in the user's words.
- **Working-backwards (PR/FAQ):** write the "it already works" outcome first — the
  press-release / demo of the finished system — then design back to today (→ 09 D1).
- **Anchor case study:** the real, cited multi-day autonomous build to reason from is the
  Boltzmann-solver case (→ 09 B). Do NOT reference `PROJECT_LAAS_v2` — it is unfindable
  (→ 09 A).
- Non-goals (explicitly: **no self-learning / weight updates** → 01).

## 2. Success criteria & evals  (→ 06)
Define this BEFORE the architecture — evals are the ratchet.
- **Eval tasks:** list them, split into Regression (single-turn) and Failure-mode
  (multi-turn).
- **Graders:** deterministic (turn count, latency, tokens) + LLM-as-judge (quality,
  tone). For each, the pass threshold.
- **Baseline & target:** the number today, the number to hill-climb to.
- **Locked feature-requirements spine (anti-premature-completion):** a *machine-readable*
  (JSON) requirements file — every requirement initially `failing`, the agent may only
  flip a `passes` field, may not remove/edit tests. JSON on purpose (model less likely to
  overwrite than Markdown). This is the "done" definition the loop grades against
  (→ 09 C4).
- **Eval layering (Hamel levels):** L1 assertions/unit tests every change · L2 human +
  model-judge on logged traces · L3 A/B with real users (→ 09 D2).
- **Banned / instant-fail outcomes (negative eval):** an explicit list of unacceptable
  results that fail immediately, regardless of the positive score (→ 10, exemplar A §12).
  Cheap, unambiguous, and catches regressions the positive rubric misses.
- **Self-score rubric anchored to references:** a per-dimension scoring matrix the maker
  fills against fixed reference targets — pairs with, does NOT replace, the independent
  verifier (→ 10 exemplar A §13).
- **Verification battery:** the concrete scripted checks a run must pass (e.g. baseline
  diffs, samples, throughput checks) — name them (→ 10 exemplar A §10).
- **Eval-maintenance rule:** how evals get updated as capability grows.
- Where eval cases live (file/format) and how a run is triggered.

## 3. Deployment target & harness  (→ 02)
- Local Claude Code, Claude Managed Agents, or hybrid — and the justification.
  (Days-long autonomy ⇒ managed/cloud tier.)
- The three resources: **Agent** (persona/model/skills), **Environment** (sandbox/
  networking/BYO-container), **Session** (binding + streamed events; lifecycle handling
  for idle/running/rescheduling/terminated).
- **Two-role split (→ 09 C2):** an **initializer** phase (run once — `init.sh`, progress
  file, initial git commit) vs. a **coding/worker** phase (every session: incremental
  progress + structured update). Define both.
- What stays thin: what you deliberately do NOT put in a custom harness.

## 4. Capabilities & decomposition  (→ 05)
For EACH capability, decide and justify: **system prompt vs skill vs custom tool vs
subagent vs MCP**, following the MCP-last rule and primitives-first.
- System prompt / `CLAUDE.md`: identity + invariants only (target length).
- Skills (progressive disclosure): list each, with its trigger and its
  `Known failure modes` section reserved.
- Tools: primitives first (bash/read/write, web search, code execution); custom tools
  only where a primitive can't do the job.
- Subagents: only for (a) fan-out or (b) fresh-mind/separation-of-duties; specify the
  exact input + expected output structure of each hand-off (comms is the failure point);
  prefer callable/managed subagents; worktree isolation for parallel writes.

## 5. Memory design  (→ 03)
- `STATE.md` (hot memory): the 5 sections (Verified facts / General rules / Open
  failures / Lessons learned / Last session).
- Memory store / directory layout; what's project-scoped (STATE) vs portable (Skills).
- **Write-before-walk** and **read-at-start** enforcement mechanism (hook? mandatory
  final loop phase?).
- **Consolidation ("dreaming"):** the scheduled pass that dedupes/fact-checks/
  restructures memory non-destructively; its cadence, model, and token budget.

## 6. Orchestration & loops  (→ 04)
- The verification loop(s): the exact circuit (produce → run → observe → fix → verify →
  done), per surface (UX/backend/E2E).
- `/loop` vs Routine vs Dynamic Workflow for each recurring job; for each Routine give
  the **Trigger / Context / Steering** triple.
- Multi-Clauding / parallelism plan and the control-plane for attention.
- Human-in-the-loop points (in the loop, not at the keyboard): where a human gates.

## 7. The self-improvement loop  (→ 07)
- The concrete produce→verify→gate→distill→write-back→consult→consolidate cycle for
  THIS system, naming the artifact each step writes to.
- Which lessons go to STATE.md vs get promoted into which skill.
- The independent-verifier design (panel size, lenses, model) and vision-verify stages.
- **Ralph-loop stop condition (→ 09 C1):** the completion gate is a re-injection loop
  (Stop-hook style) that kicks the agent back in on claimed completion and only exits when
  a **numeric / rubric criterion** passes (e.g., the locked feature-requirements file is
  all-`passes`). Specify the exact criterion — never a subjective "done."

## 8. Model routing & safety  (→ 08)
- The role→model table for this system.
- Classifier-block fallback routing (→ Opus / human) and per-skill notes.
- Credentials (vault/secret handling — never in prompts/memory), session deletion,
  data-retention policy for autonomous runs.

## 9. Milestones — minimal viable compounding first  (→ 07)
- **M0:** `CLAUDE.md` + `STATE.md` + one skill + one maker/verifier loop with a rubric.
- **M1:** eval suite + nightly write-back routine.
- **M2+:** expansion (multi-Clauding, dreaming at scale, subagent fan-out, event triggers).
Each milestone states its eval target (hill-climb checkpoint).
- **Phase-gated roadmap (→ 10 exemplar A §11):** structure milestones as ordered phases,
  each with an explicit **closing gate** that must pass before the next phase opens.
- **Single final acceptance test (→ 10 exemplar A §15):** one objective, human-legible
  "ship it" gate for the whole system, separate from per-phase gates.

## 10. Risks & open questions
- Explicit `[ASSUMPTION]`s and how each will be verified (turned into `[VERIFIED]`).
- Failure modes anticipated (context bloat, orchestrator↔subagent comms, contradictory
  policy, silent classifier blocks) and the design that prevents each.

## 11. Appendix
- Glossary, links to the context files used, and any templates (rubric file, STATE.md
  starter, skill skeleton) the plan references.

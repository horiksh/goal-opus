# Context Pack — Self-Improving Agent System

**Purpose.** This directory is the reading context for a planning model (Fable 5)
that will design a *self-improving agent system*. It is not the plan. It is the
ground-truth substrate the plan must be built on. Read this file first, then load
the numbered files on demand (progressive disclosure — don't pull all of them into
context at once; open the one the current planning decision needs).

---

## How to use this pack (for the planning model)

1. Read this README fully. It sets the mission, the epistemic rules, and the map.
2. Read `01-mission-and-definitions.md` to lock the goal and the self-improving vs.
   self-learning distinction.
3. When planning a specific layer, open the matching file:
   - Harness / infrastructure decisions → `02-cma-primitives-and-harness.md`
   - Memory design → `03-memory-and-dreaming.md`
   - Loops, scheduling, remote runs → `04-orchestration-loops-routines.md`
   - "Should this be a tool, a skill, or a subagent?" → `05-tool-skill-subagent-decomposition.md`
   - Measuring progress → `06-evals-and-hill-climbing.md`
   - The compounding loop itself → `07-self-improvement-loop.md`
   - Which model runs what, and safety fallbacks → `08-model-routing-and-safety.md`
   - External case studies + PRD methodology → `09-case-studies-and-prd-methodology.md`
   - Real inspected example projects + exemplar artifacts → `10-usage-case-examples.md`
4. Produce the plan by filling `PRD-TEMPLATE.md`.

---

## Epistemic rules (READ — this is the most important section)

This project is *about* the discipline of separating verified facts from guesses.
The context pack must practice it. Every claim in these files is tagged:

- **[VERIFIED]** — grounded in a primary source cited in `09-...` or in Anthropic's
  own Code w/ Claude engineering talks (transcript supplied by the project owner).
  These are engineering patterns you can plan around.
- **[TALK]** — stated in the Code w/ Claude talks as illustration (e.g., a specific
  eval percentage or latency number from a live demo). Treat as *directionally true
  and pattern-valid*, but do NOT hard-code the exact number as a guarantee.
- **[LORE]** — from a third-party Substack post ("14-step roadmap"). Marketing
  framing that could NOT be verified. **Do not plan around any [LORE] claim.**
  Listed only so the plan doesn't accidentally inherit it.

### Known [LORE] to ignore
The originating Substack post asserted, without a verifiable source:
- "Mythos-class model," "Project Glasswing," a "319-page system card."
- Named experiments "Parameter Golf" and "Continual Learning Bench 1.0" with exact
  numbers ("73% vs 17% verification coverage," "~6× more improvement," "8×H100 for
  8 hours").
- Exact pricing ("$10/$50 per M tokens"), an exact launch date, and quotes attributed
  to named Anthropic engineers.

None of these are load-bearing. The *architecture* they wrap (loops with an
independent grader, memory that compounds, skills that accumulate, scheduled cloud
runs, verification loops) is real and is documented from the talks below. Build on
the architecture, not the lore.

**Correction — `PROJECT_LAAS_v2` resolved [UNFINDABLE → VERIFIED].** An earlier research
pass could not find "PROJECT_LAAS_v2" and marked it unfindable. With a repo link from the
project owner it is now verified: it is **`PROJECT_LAAS_v2.md`, the spec file inside the
repo `Braffolk/fable5-world-demo`** (a real ~99%-Fable-5-built 3D world demo) — not a
standalone project, which is why a name search missed it. See
`10-usage-case-examples.md`. (The lesson stands: a name stayed a guess until a *primary
source* resolved it — don't fabricate either way.)

### Model-name corrections
The Substack post used stale names ("Sonnet 4.6," "Opus 4.7"). Use the real IDs
available in this environment: `claude-fable-5`, `claude-opus-4-8`, `claude-sonnet-5`,
`claude-haiku-4-5`. (The talks predate these and reference `claude-3.5-opus` /
`opus-4.7` — read those as "the current frontier orchestrator model of the day.")

---

## Primary source

The core engineering patterns in files 02–07 are distilled from Anthropic's
**Code w/ Claude** sessions (transcript provided by the project owner):
- **Session 1 — Ship Your First Managed Agent** (Isabella He): CMA primitives,
  brain/hands decoupling, server-side loop, incident-response agent.
- **Session 2 — Agents That Remember** (Kevin Chen): Memory Stores, Dreaming.
- **Proactive Agents / Routines** (Maya Nielan) and **Stop Babysitting Your Agents**
  (Sid Bidasaria): verification loops, `/loop`, routines, multi-Clauding, remote control.
- **Tool, Skill, or Subagent?** (Will): agent decomposition, progressive disclosure,
  primitives-first tooling, eval hill-climbing.

Where these are corroborated by public Anthropic docs, `09-...` carries the citation.

**Cited external corroboration (added in `09-...`).** A fan-out/verify research pass found
that primary Anthropic engineering posts independently confirm the transcript's core
patterns — persistent state files as portable memory, an editable `CLAUDE.md`,
"context engineering," a loop-to-numeric-criterion ("Ralph loop"), a locked JSON
feature-requirements eval file, and a two-role initializer/coding harness — plus one real
multi-day case study with a source. That agreement is why files 02–07 can be trusted as
plan foundations, not just talk notes. See `09-case-studies-and-prd-methodology.md`.

A further pass (`10-usage-case-examples.md`) adds **inspected example projects**: the
Braffolk Fable-5 world demo (with its real spec + memory files), Anthropic's 16-agent
C-compiler build, a three-agent Planner/Generator/Evaluator app harness, a
self-improving-skills plugin, and — most usefully — an **official reference harness
(`anthropics/cwc-long-running-agents`)** that implements this pack's loop as copyable hooks.

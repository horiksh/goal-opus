# Agent home — self-improving goal-loop system

This repo hosts `/goal-opus` (self-improving generator/evaluator loop) and `/prd`
(research-first PRD generator that feeds it). Design substrate: the context pack in
`docs/context/` (files 01–10). Intended flow: `/prd` defines done → `/goal-opus`
builds to it.

## Invariants (always apply)

- **Compounding contract:** every output is graded by an independent verifier, the
  confirmed lesson is distilled into a general rule, and the rule is written back to
  durable memory or a skill — so the next run inherits it.
- **Read at start:** at session start, read `STATE.md` and follow its
  `## Rehydration protocol` before doing project work.
- **Maker ≠ grader:** the agent that produced work never grades it. The verifier
  (`goal-verifier`) never edits files. Only the orchestrator writes `criteria.json`.
- **Write before walking:** a `/goal-opus` run is not finished until its write-back
  phase (Phase 6) has run — on success, abort, or cancel alike.
- **No self-learning:** improvement means editing files (STATE.md, skills, rubrics),
  never assuming the model itself changes between runs.

- **PRDs never contain code:** `/prd` produces documents and a seeded rubric only;
  building happens in `/goal-opus`.
- **This repo is the agent HOME, never a build target:** product code lives in each
  goal's TARGET repo; only the system, its memory, and run evidence live here.
- **Visual work is verified by LOOKING:** any goal whose deliverable is visual runs
  vision-verify (re-captured screenshots judged against frozen references/baselines);
  text-only verification of visual work is banned.
- **Primitives-first retrieval:** maker/verifier search via grep/Glob/Read over live
  files — no embedding/RAG index (Anthropic dropped it for agentic grep; needless dep at
  this corpus size) and no persistent maker-side code-graph (a self-rewriting maker
  staleness-invalidates any index each iteration). Evidence + the sole verifier-only
  exception: `docs/context/11-retrieval-invariant.md`.

Procedures live in `.claude/skills/goal-opus/SKILL.md` and
`.claude/skills/prd/SKILL.md` — do not duplicate them here.

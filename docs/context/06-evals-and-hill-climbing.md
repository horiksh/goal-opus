# 06 · Evals & Hill-Climbing

Source: "Tool, Skill, or Subagent?" (Will) + verifier-subagent pattern.

## Hill-climbing is the improvement method  [VERIFIED — talk]

The core loop Anthropic uses internally:

```
establish an eval baseline → change the architecture → re-run evals → keep what climbs
```

Without evals, a loop stops at "handled enough"; with evals, every architecture change
is measured, so the system improves over time instead of drifting. **Evals are the
objective stop condition and the ratchet.** In the worked example this took the agent
from a low baseline (~62–83% depending on the run) to ~92%.

**Corollary:** update the evals as the product's capability expands. Evals must keep
encompassing what you actually care about, or you hill-climb the wrong hill.

## The grader taxonomy  [VERIFIED — talk]

The example agent used **12 eval tasks across 5 grader types**, split two ways:

**By task shape:**
- **Regression (R…)** — realistic *single-turn* tasks: give a task, model comprehends,
  calls tools, responds; grade the response.
- **Failure-mode (F…)** — more complex *multi-turn* tasks graded end to end.

**By grader mechanism:**
- **Deterministic** — turn count, latency, token usage. Tracked over time.
- **Non-deterministic (LLM-as-judge)** — personality, tone, style, output quality.

Design consequence: the plan needs *both* — cheap deterministic metrics to catch
efficiency/cost regressions, and an LLM judge for qualitative dimensions. Track the
deterministic ones as time series (a regression in tokens/turns/latency is a real
regression even if the answer is "right").

## Diagnose failures with the model itself  [VERIFIED — talk]

A reliable technique: run the evals *inside* Claude Code (via bash) and have Claude
triage the failures into themes/root causes. In the talk this surfaced exactly the
`05-...` failure signatures: model doing work it should have a tool for, output-structure
mismatches between subagents and orchestrator, and conflicting policies in a bloated
system prompt.

## Verifier subagent > self-critique  [VERIFIED — pattern]

**Do not let the maker grade its own work.** A model reviewing its own output sees its
own reasoning trail and prefers conclusions consistent with what it already wrote. An
independent verifier sees only the *artifact + the rubric* — no skin in the maker's game.

Structural rules for the plan:
- The agent that produced the work is **never** the agent that grades it.
- The verifier receives the artifact and an explicit rubric, and is prompted to *refute*
  / find gaps by default (adversarial), not to rubber-stamp.
- For robustness, use an odd panel (e.g., 3 independent verifiers, majority rules) and,
  where a finding can fail in multiple ways, give each verifier a distinct lens
  (correctness / does-it-reproduce / policy).
- Graders can run on a cheaper model (independent context, low cost) — the verifier role
  does not need the frontier model. See `08-...`.
- **Concrete implementations to copy (→ 10):** the fresh-context evaluator subagent (with
  *no* Write/Edit tools) in `anthropics/cwc-long-running-agents`, and the Playwright-driven
  evaluator in Anthropic's three-agent app harness — both are working versions of this
  section from primary sources.

## Vision self-check for visual work  [VERIFIED — pattern]

Where the output is visual (UI, dashboards, charts, design fidelity), the verifier must
*look*, not read a text description:
- Maker writes the UI and renders it to a screenshot.
- An independent vision-capable verifier compares the screenshot to the goal, to design
  tokens in the project skill, and to the previous screenshot in STATE.md.
- Verdict → loop: match ⇒ done; mismatch ⇒ structured diff back to the maker.

Text-only verification of visual work misses the exact failure mode that matters. Any
loop whose deliverable is visual must include a vision-verify stage.

## The Outcomes/rubric pattern (objective completion)  [VERIFIED — feature]

For long/hosted runs, define a **rubric of gradable criteria** and a **hard
max-iterations bound**; an independent grader checks the artifact each iteration, a
"not-met" verdict starts the next iteration, and the loop exits when the grader passes
(or the bound is hit). This is the same maker≠grader shape as a local goal loop, sized
for hours-to-days runs. The plan should specify the rubric file format and where it lives.

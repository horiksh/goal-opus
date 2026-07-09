# 08 · Model Routing & Safety Fallbacks

## Route by task complexity, not by default  [VERIFIED — pattern]

The frontier orchestrator model is expensive; most steps in a self-improving system
don't need it. Route roles to tiers, using the real IDs in this environment:

| Role | Model | Why |
|---|---|---|
| **Orchestrator** | `claude-fable-5` | multi-stage planning across a long horizon, delegating to subagents, distilling rules from accumulated evidence, days-long stamina |
| **Hard, bounded subtasks** | `claude-opus-4-8` | architecture decisions, complex debugging, deep code review; also the explicit fallback for classifier-blocked requests |
| **High-volume workers** | `claude-sonnet-5` | refactors, test scaffolding, doc updates, lint passes — the bulk of fan-out |
| **Graders / classifiers** | `claude-haiku-4-5` | independent verifier role — cheap, independent context window |

The economical pattern: **orchestrator on Fable 5, workers on Sonnet, graders on Haiku,
fall back to Opus** for the hard-bounded and the blocked. Set the model *per agent*
(the `Agent` tool and Workflow `agent()` both take a model override); default the
orchestrator to inherit the session model, override only where a different tier clearly
fits.

Cost discipline note: the verifier role (`06-...`) is deliberately a *separate, cheaper*
model — independence matters more than raw capability for grading, and it keeps the
adversarial-panel pattern affordable.

## Design the safety boundary as a known fallback, not a failure mode  [VERIFIED — principle]

A frontier model may **decline** in specific high-risk domains (e.g., certain
cybersecurity vulnerability research, and bio/chem areas). In an autonomous loop, a
silent decline looks identical to a real error — until you debug it.

Architect for it explicitly:
- If a task may touch security tooling (SAST, exploit logic, some crypto-primitive code
  review) or bio/chem, **route it to a fallback model (`claude-opus-4-8`) or escalate to
  a human reviewer** — don't let the loop treat a decline as a retryable failure.
- Give each skill a note on which of its tasks may hit a classifier and what the expected
  fallback behavior is, so the loop handles it gracefully rather than looping on it.
- Treat the boundary as an interface that can change: explicit handling stays robust when
  the policy evolves; ignoring it produces silent regressions on the next policy update.

## Credentials & data handling  [VERIFIED — talk]

- Keep secrets in the credential layer (CMA **Vaults** / OS credential store /
  gitignored env), **never in prompts or memory files**. The brain/hands decoupling
  (`02-...`) exists precisely so the loop never handles raw, unencrypted credentials.
- **Delete sessions** when done so no unneeded data is retained in the cloud.
- Before routing sensitive data through a scheduled cloud routine, check the applicable
  data-retention terms. The plan should state what data classes are allowed through
  autonomous runs and what must stay local / human-gated.

## Token-cost controls  [VERIFIED — talk]

- Prompt caching is the main lever (consolidation/dreaming runs report ~95% cache hits).
- Prefer **code execution over context-stuffing** for large data (`02`, `05`) — the
  biggest single token lever observed (>200k → a fraction on a data task).
- Use progressive disclosure (skills) so the context window isn't polluted with info the
  current task doesn't need.
- For heavy async jobs, schedule them where a batch/off-peak discount applies and cap
  with a token budget.

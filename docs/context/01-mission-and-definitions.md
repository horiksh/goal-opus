# 01 · Mission & Definitions

## The mission

Design a **self-improving agent system**: not a chat you prompt for five minutes, but
a system in which *every run leaves the next run smarter*. Each session writes verified
lessons to durable memory; each skill sharpens as edge cases accumulate; each state
file gains facts the system stops re-deriving. The model is stateless between runs —
**the system around it is what compounds.**

The plan this pack feeds must produce a system that can:
- Run long-horizon, multi-stage work (hand off a project, review the deliverable).
- Verify its own work with an *independent* grader, not self-critique.
- Persist and consolidate memory across sessions.
- Improve its own skills/rules from real failures.
- Run without a human at the keyboard (scheduled / event-triggered), while staying
  watchable, steerable, and bounded.

## Self-improving ≠ self-learning  [VERIFIED — definitional]

- **Self-learning** = the model updates its own weights from experience. **No shipping
  model does this in production.** Do not plan for it. It is not on the table.
- **Self-improving** = the *environment* around a fixed model compounds: memory files
  accumulate verified facts, skills gain failure-mode sections, eval loops refine
  prompts and rubrics. This is a property of the **system you build**, not the model.

Design consequence: every capability in the plan must be expressible as *state that
survives a session* (a file, a skill edit, a memory-store entry, an eval case) — not
as a hoped-for change in the model.

## The compounding contract

The single invariant the whole system must preserve:

> **Every output is graded by an independent verifier, the confirmed lesson is
> distilled into a general rule, and the rule is written back to durable memory /
> a skill — so the next run inherits it.**

If a session ends without a write-back, that run's learning is lost and the system
degrades to a fast chat tool. The plan must make write-back structural (a hook, a
required final phase of every loop, or a scheduled consolidation job), never a matter
of discipline.

## Non-goals / anti-patterns to design out  [TALK]

From the Code w/ Claude talks, the failure modes that keep such a system at a fraction
of its potential:
- Using the frontier model like a faster chat tool (prompt-and-close), no compound effect.
- Self-critique instead of an independent verifier.
- No durable state file → every session restarts from zero.
- Skills that never get written back to after a real failure.
- Frontier model on tasks a cheaper worker model handles (route by complexity).
- Long-horizon sessions pinned to a laptop (must run on cloud/managed infra).
- Silent failure on a safety-classifier block (architect the fallback explicitly).
- Text-only verification of visual work (use vision self-check where output is visual).
- Loops with no objective stop condition (they stop at "good enough," not "done").

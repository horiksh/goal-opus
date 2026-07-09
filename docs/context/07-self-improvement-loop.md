# 07 · The Self-Improvement Loop (how it all compounds)

This file ties files 02–06 into the single feedback loop that makes the system
self-improving. It is the heart of the plan.

## The compound stack (build bottom-up; leverage compounds upward)

```
Layer 4 · Self-improvement   vision self-check · eval hill-climbing · rule distillation · dreaming
Layer 3 · Memory             STATE.md / memory store · Skills · consolidated (dreamed) memory
Layer 2 · Orchestration      verification loops · /loop · Routines · Dynamic Workflows · Outcomes
Layer 1 · Primitives         Fable 5 + subagents · bash/read/write · web search · code execution · worktrees
```

Every output from Layer 1 flows up to Layer 4, where it is graded, distilled, and
written back to Layer 3. Tomorrow's Layer-1 run inherits the sharpened memory and
skills. **The model is stateless; the system isn't.**

## The loop, concretely

```
1. PRODUCE   maker agent does the task (Layer 1–2)
2. VERIFY    independent verifier grades artifact vs rubric (adversarial;
             vision-verify if visual)                                   → 06
3. GATE      pass → ship / mark done;  fail → structured diff back to maker, iterate
4. DISTILL   turn the confirmed lesson into a GENERAL rule              → 03 stage 4
5. WRITE-BACK
             - project-scoped, in-progress  → STATE.md
             - confirmed & general           → promote into a Skill (procedural memory)
             - a failure the loop hit         → add to the skill's "known failure modes"
6. CONSULT   next run reads STATE.md + relevant skills at start         → 03 stage 5
7. CONSOLIDATE (async, scheduled)
             a dreaming/consolidation routine dedupes, fact-checks, and
             restructures memory so it stays readable as it grows       → 03
```

Steps 4–5 are the ones teams skip; they are what make it compound. Make write-back
**structural**: a required final phase of every loop, a stop hook, or the job of the
scheduled consolidation routine — never left to discipline.

## Self-improving skills (procedural memory that sharpens)  [VERIFIED — talk]

The highest-leverage compounding artifact. After any non-trivial failure, **write the
lesson into the skill itself**, not just the chat/STATE.md. Over weeks a skill grows new
sections it didn't start with:
- `## Known failure modes` — added by the loop over time (with the fix).
- `## Anti-patterns (do NOT do)` — added after real incidents.
- `## Eval suite` — cases the loop verifies the skill against.

The explicit instruction that makes a skill self-improving (from the talk): *"Every time
you hit a blocker, edit your own skill file to document the solution for next time."*
The whole team contributes; a two-week-old skill materially outperforms what the model
derives from scratch on a fresh project.

## Dreaming as the memory-consolidation half of the loop  [VERIFIED — talk]

Live write-back keeps memory *current*; **dreaming keeps it *clean***. Schedule an async
consolidation pass (a routine) that takes the memory store + recent transcripts and
distills/fact-checks/dedupes into a structured, non-destructive output store with a diff
to review. Without it, memory grows into an unreadable dump and stops being consulted.

## What "done improving" never means

There is no terminal state — but there IS an objective stop condition *per task*: the
verifier's rubric passing (or the Outcomes max-iteration bound). The system is
"improving well" when: verification coverage is high (most claims are checked, not
guessed), skills gain failure-mode sections from real incidents, the eval baseline
climbs release over release, and memory stays consultable after consolidation.

## Minimal viable compounding (what to ship first)

Don't build all four layers at once. Ship the smallest loop that compounds:
1. `CLAUDE.md` + `STATE.md` with the 5-section schema (Layer 3 hot memory).
2. One maker→independent-verifier loop on a real task, with an objective rubric (Layer 2+4).
3. One self-improving skill with a `Known failure modes` section (Layer 3 procedural).
4. Then: one scheduled routine that re-runs evals and writes back nightly (Layer 4 async).

Everything else (multi-Clauding, dreaming at scale, callable-subagent fan-out) is
expansion once this core loop demonstrably compounds.

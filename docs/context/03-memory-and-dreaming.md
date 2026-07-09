# 03 · Memory & Dreaming

Source: Code w/ Claude S2 (Kevin Chen), plus the memory-progression framing.

## The problem: sessions are silos  [VERIFIED — talk]

By default each session is isolated — the agent has amnesia. Tell it a fact in one
session, ask about it in the next, and it has no idea. Memory is the first thing that
turns a set of runs into a system.

## Three composable memory layers  [VERIFIED — talk]

Plan memory as three layers, each augmenting the one below:

1. **Session** — one ephemeral conversation/instance of the agent.
2. **Memory Store** — a persistent, filesystem-like store attached to sessions as a
   resource. The model gets tools (bash, grep, read, write) to read/write it, so facts
   carry *across* sessions. (CMA CLI: `ant beta:memory-stores create --name ... --description ...`.)
3. **Dreaming** — an async batch process that *organizes, enriches, dedupes, and
   staleness-checks* the store over time, so it doesn't grow into an unreadable dump.

Locally, layer 2 = `STATE.md` + the memory directory; layer 3 = a scheduled
consolidation routine (see `04-...`).

## Dreaming: consolidate transcripts into structured memory  [VERIFIED — talk]

Memory stores grow unbounded and disorganized: agents dump raw notes, duplicates
accumulate, facts go stale. **Dreaming** is a specialized batch harness that:
- takes an **input memory store + a list of prior session transcripts**,
- distills new information, **fact-checks**, and **deduplicates**,
- writes into a **cloned OUTPUT memory store** (non-destructive — the input is never
  edited in place),
- produces a **diff** for optional human-in-the-loop review before you attach the
  output store to future sessions,
- turns raw conversation history into structured, retrievable markdown (index files,
  event logs, entity/speaker lists) that future agents read efficiently.

Operational notes from the talk: dreaming is **exhaustive by design → token-heavy**,
but **~95% of tokens are cached**; a Batch-API-style ~50% scheduled discount was being
explored. Token controls: switch the model, steer the prompt (custom instructions like
"organize files with this structure" or "focus on fixing these details"), and budget.

**Design consequence:** separate *hot* memory (written live during a session) from
*consolidated* memory (produced by an async dreaming/consolidation pass). Never let the
live write path be the only thing keeping memory clean — schedule consolidation.

## The 5-stage memory progression (what "good memory" means)  [VERIFIED — pattern]

Effective memory is a progression, not a note dump. Each stage is a structural move:

1. **Fail** — get something wrong; document the failure with enough detail to be useful.
2. **Investigate** — figure out *why* before moving on.
3. **Verify** — turn the diagnosis into a *checked fact*, not a guess.
4. **Distill** — turn the verified fact into a *general rule* beyond the specific case.
5. **Consult** — on the next task, *read the rule* instead of re-deriving it.

A note store that only ever reaches stage 1 ("maybe it's X? unsure") does not compound.
The plan should make stages 3–4 (verify, distill) explicit steps, and stage 5 (consult)
automatic at session start.

## STATE.md schema (local hot-memory file)

The plan should specify a state file with sections mapped to the progression:

```markdown
# Project memory · <system name>

## Rehydration protocol   # read-me-first: how the next session resumes (→ validated by 10)
## Verified facts        # stage 3 — stop guessing about these (each with how it was verified)
## General rules         # stage 4 — consult before re-deriving
## Key decisions log     # ADR-style D1, D2… — WHY an architecture choice was made (→ 10)
## Open failures         # stages 1–2 — in progress, with repro steps / file links
## Lessons learned       # stage 4 distillations (candidates to promote into Skills)
## Last session          # stage 5 — resume pointer: what was tried/passed/failed, next step
```

The `Rehydration protocol` and `Key decisions log` sections were added after inspecting a
real production `STATUS.md` (→ `10-usage-case-examples.md`, exemplar B), whose 12-section
durable-memory file is a superset of this schema. The decisions log is distinct from
`Verified facts`: it records *why a choice was made* so it isn't relitigated.

Two operating rules that decide whether it compounds or just grows:
- **Write before walking away.** Every session ends by updating STATE.md. Make it a
  hook or the mandatory final phase of every loop — not discipline.
- **Read at session start.** Every session begins by reading STATE.md + the most
  relevant skills. Without this, even a strong model regresses to amnesiac behavior.

## STATE.md vs Skills (scope)  [VERIFIED — talk]

- **STATE.md / memory store = project memory.** Scoped to this system; dies with it.
- **Skills = procedural memory.** "How to do this kind of thing," portable across
  projects, in `~/.claude/skills/`. Confirmed, general lessons get promoted from
  STATE.md into a skill so they travel. See `05-...` and `07-...`.

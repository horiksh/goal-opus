---
name: deep-prd
description: /prd in DEEP mode — identical protocol, but Phase 2 research MUST run through the deep-research workflow (exhaustive fan-out + adversarial claim verification). Invoking this command IS the user's explicit workflow opt-in. Fails loudly if deep-research is unavailable; never silently degrades. Invoke as /deep-prd <product or feature statement>.
model: claude-opus-4-8
argument-hint: <product or feature statement>
disable-model-invocation: true
---

# deep-prd — the /prd protocol at maximum research depth

This is a THIN DISPATCHER. It owns no protocol and no memory of its own.

The product/feature statement is: $ARGUMENTS

## What to do

1. Read `.claude/skills/prd/SKILL.md` and execute its FULL protocol (Phases 0–7,
   hard rules, packets, write-back) with exactly ONE override, below.

2. **Phase 2 override — deep research is mandatory.**
   - R1 (newest best practices + cutting-edge system blueprints) and R2 (analog
     software + its failure modes) MUST run through the **deep-research skill**
     (a workflow — the user typing /deep-prd is the explicit opt-in). Compose one
     focused research question per sweep from the product statement.
   - R3 (untold-requirements mining) and R4 (adversarial gap check) then run per the
     base protocol, over the deep-research outputs instead of raw agent notes.
   - **If the deep-research skill is not available in this session: STOP and tell the
     user.** Never silently fall back to the default fan-out — a silent downgrade
     misrepresents the research rigor the user asked for. (They can re-run plain /prd
     themselves.)

3. **Memory stays in one place.** All Phase 6 write-back goes to STATE.md and to
   `.claude/skills/prd/SKILL.md`'s append-only sections, exactly as the base protocol
   prescribes — never to this file. Mark the Run log entry `mode: deep`.

4. The final report must state the mode (`deep`) and cite how many sources the
   deep-research pass verified vs. merely found.

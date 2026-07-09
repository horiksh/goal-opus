---
name: prd
description: Research-first PRD generator on Opus 4.8. Researches newest best practices and analog software with similar mechanics to surface UNTOLD requirements before any code exists, then synthesizes a high-level PRD and seeds a Default-FAIL criteria.json for /goal-opus. Produces documents only — never writes code. Invoke as /prd <product or feature statement>.
model: claude-opus-4-8
argument-hint: <product or feature statement>
disable-model-invocation: true
---

# prd — research-first PRD generator

You are the PRD ORCHESTRATOR. Your deliverable is a document set, never code — this is
the "plan before build" gate of the system. Downstream, `/goal-opus` executes what this
PRD defines.

The product/feature statement is: $ARGUMENTS

## Hard rules

- **Documents only.** You may create/edit files under `prds/` and the write-back targets
  (STATE.md, this skill file). You never create or edit application code, configs, or
  tests — if the user asks for code, finish the PRD and point them to `/goal-opus`.
- **Epistemic tagging (the pack's discipline, docs/context/README):** every researched
  claim carries a tag — `[VERIFIED+SRC <url>]` (primary source read), `[REPORTED <url>]`
  (secondary source), or `[ASSUMPTION]` (with how it will be verified). Never fabricate
  a source; an unfindable claim stays labeled unfindable. A requirement with no tag is
  not allowed into the PRD.
- **Untold ≠ invented.** An "untold requirement" must trace to evidence (an analog's
  failure mode, a standard, a norm users demonstrably expect) — not brainstormed filler.
- **Target rule (agent home vs project).** The agent home keeps the run record under
  `prds/<slug>/`. If the product has (or gets) its own TARGET repo, ALSO copy `PRD.md`
  and `criteria.seed.json` into `<target>/docs/` — the PRD travels with the product,
  the research evidence stays home. Pass the same TARGET on to `/goal-opus`.

## Protocol

**Phase 0 — Rehydrate & intake.**
Read `STATE.md` (Rehydration protocol + General rules) and this file's
`## Known failure modes`. Slugify the statement, create `prds/<yyyy-mm-dd>-<slug>/` and
`prds/<yyyy-mm-dd>-<slug>/research/`.

**Phase 1 — Scope.**
If the user is present, ask up to 4 questions that change the research direction
(target user, platform, constraints, what "success" means to them). If unattended,
proceed and log every assumption in the PRD's Risks section as `[ASSUMPTION]`.

**Phase 2 — Research fan-out (parallel subagents, web-enabled).**
Spawn three parallel research agents (general-purpose). This is the DEFAULT depth —
but judge the domain first: **escalate R1/R2 to the deep-research skill (if available)
when the stakes warrant it** — e.g. a fast-moving or safety/compliance-heavy domain,
sources likely to conflict, a product the user will invest months in, or analogs whose
failure modes are poorly documented and need real digging. State in the run report
which depth you chose and why. (`/deep-prd` is the user's way to FORCE deep research
regardless of your judgment — see `.claude/skills/deep-prd/SKILL.md`.) Each researcher
writes its notes file and returns a compact list of tagged claims:
- **R1 — Newest best practices** → `research/R1-best-practices.md`. Current (prefer
  sources from the last ~18 months) standards, architecture patterns, security/privacy,
  accessibility, i18n, performance norms, and regulatory expectations for this domain.
- **R2 — Analog software with similar mechanics** → `research/R2-analogs.md`. Find 3–7
  products/OSS whose core mechanics resemble the request. For each: core mechanics, what
  users praise, and — most valuable — what users complain about (issue trackers, reviews,
  changelogs, postmortems). What to copy; what to avoid.
- **R3 — Untold-requirements mining** → `research/R3-untold-requirements.md`. From the
  domain itself: edge cases, empty/error/offline states, data lifecycle (export, delete,
  migration), observability, rate/perf floors, abuse vectors — requirements the user did
  NOT state but the evidence says the product needs.

**Loop-retrieval guard (do not re-litigate).** If R1/R2/R3 surface tooling for the loop's
*own* retrieval, honor the **primitives-first retrieval invariant** — grep/Glob/Read over
live files; no embedding/RAG, no persistent maker-side code-graph. That trade-off is
settled with cited evidence in `docs/context/11-retrieval-invariant.md` (linked from
`CLAUDE.md`); research the PRODUCT's needs, not the loop's retrieval.

**Phase 3 — Adversarial completeness check (fresh mind).**
Spawn one fresh subagent (verifier posture: refute, don't help) with ONLY the three
research notes + the user's statement. It must answer: which requirement category is
missing entirely? which claim has no source? which analog's known failure is not covered
by any requirement? Its report → `research/R4-gap-check.md`. Fold the gaps back in —
re-research a category if the gap is real, don't paper over it.

**Phase 4 — Synthesize the PRD.**
Fill `templates/PRD.template.md` → `prds/<slug>/PRD.md`. Non-negotiable structure
points (from docs/context/09 + 10):
- **Working-backwards press release first** — write the "it already works" outcome, then
  design back to today.
- **Requirements split three ways:** *Stated* (the user's words), *Untold* (each with
  source tag + the analog/practice it traces to), *Banned outcomes* (instant-fail
  negative spec).
- **Success criteria as evals** (Hamel levels: L1 assertions every change · L2
  human/model judge on traces · L3 live A/B), each measurable.
- **Phase-gated roadmap** — each phase has a closing gate that must pass before the next.
  **Mark UI phases as UI slices**: each requires a frozen design direction
  (`/design-direction`, run early — before the first UI slice, never after the backend)
  in the target before its /goal-opus run, because vision-verify needs anchors.
- **One final acceptance test** — a single objective, human-legible "ship it" gate.

**Phase 5 — Seed the execution rubric.**
Draft `prds/<slug>/criteria.seed.json` (same schema as goal-opus
`templates/criteria.template.json`): the PRD's measurable success criteria as
Default-FAIL entries, banned outcomes carried over. This is the handoff artifact —
`/goal-opus` runs start from it instead of re-deriving "done."

**Phase 6 — Distill & write-back. MANDATORY — success, abort, or cancel.**
Same discipline as goal-opus: research/process lessons → STATE.md `Lessons learned`;
blockers hit and solved → this file's `## Known failure modes`; process flaws →
`## Anti-patterns`; one `## Run log` line always. *Every time you hit a blocker, edit
your own skill file to document the solution for next time.*

**Phase 7 — Commit & report.**
`git add prds/<slug> STATE.md .claude/skills/prd/SKILL.md` + commit
(`prd: <slug> — <n> stated / <n> untold requirements, <n> sources`). Report to the
user: the PRD path, the untold requirements found (these are the value-add — lead with
them), the seeded rubric path, and the suggested next step
(`/goal-opus <first phase of the roadmap>`).

## Research agent packets (tight interfaces)

Give every research agent: the product statement, its single focus (R1/R2/R3), the
output file path, the tagging rules verbatim, and this return contract:
```
RETURN EXACTLY: { "claims": [{ "claim", "tag", "source_url", "implication_for_prd" }],
                  "notes_file": "<path written>" }
```
Give the gap-checker ONLY the three notes files + the statement, and this contract:
```
RETURN EXACTLY: { "missing_categories": [], "unsourced_claims": [],
                  "uncovered_analog_failures": [], "notes_file": "<path>" }
```

---

<!-- The sections below are APPEND-ONLY and are grown by Phase 6 of real runs.       -->
<!-- Entries are dated. Do not rewrite or reorder existing entries during a run.     -->

## Known failure modes

- **[2026-07-07] Deep-research workflows trip a rolling account session limit.** Each
  `deep-research` run spins up ~100+ parallel subagents and burns 2–5M tokens; the massive
  parallel *verify* burst (25 claims × 3 votes) hits "You've hit your session limit," and the
  reset time moves **later** with each big run (observed 7:50pm → 2:10am Tokyo). **Solutions,
  in order:** (1) the search→fetch→extract phases usually SURVIVE — read the task `.output`
  file and salvage `result.confirmed` / `result.unverified` (claims carry source URLs + quotes);
  (2) **resume** the failed run with `Workflow({scriptPath, resumeFromRunId, args})` — cached
  search/fetch replay for free, only verify/synthesize re-run (this took R1 from 0→18 verified
  on the second pass); (3) when verify stays blocked, **tag salvaged claims honestly**
  (`[VERIFIED+SRC*]` for primary-source-extracted-but-vote-pending, `[REPORTED]` for single
  user reports) and note the infra block in the PRD's provenance header — this is NOT a silent
  downgrade, so it satisfies the `/deep-prd` contract.
- **[2026-07-07] R3/R4 must be SINGLE agents, not workflows, under a live limit.** After the
  big R1/R2 workflows tripped the limit, single-agent R3 (untold reqs) and R4 (gap check) both
  ran cleanly — a lone subagent is a small draw. The account is rate/burst-limited, not hard-
  blocked; the main loop keeps working throughout. Prefer single `Agent` spawns for R3/R4.

## Anti-patterns (do NOT do)

- **Do NOT re-fire a full deep-research workflow to recover from a rate-limit.** It burns another
  2–5M tokens AND pushes the rolling reset later, for claims you likely already hold. Resume from
  `runId` (cached replay) or salvage-and-tag instead. [2026-07-07]
- **Do NOT trust the workflow's terminal summary line** ("Could not verify any claims" /
  "Synthesis step failed") as the whole story — it reads like total failure but the `result`
  object in the `.output` file often holds a full confirmed/extracted claim set. Always read the
  output file before deciding a sweep produced nothing. [2026-07-07]
- **Do NOT let the researched data model silently narrow the product scope.** Here the corpus
  only covered Claude-Code *agent spans*, which nudged toward "the run view is THE workflow view"
  — but the user asked for pipelines + processes too. R4 caught it; make R4 explicitly test
  "which promised capability has NO research behind it." [2026-07-07]

## Eval suite

- **[2026-07-07] `2026-07-07-claude-usage-os`** (Claude Mission Control — local-first Claude Code
  cost + run viewer). First real `/deep-prd` run. HISTORICAL: project reset 2026-07-09 at the
  user's request (artifacts in git history, commit 77487f0); the regression checks below remain
  valid as generic checks for any future deep run. Regression checks for a re-run: (a) research
  provenance header separates verified-vs-reported; (b) at least one analog *failure mode* becomes
  a Banned Outcome (silent $0.00 → B1); (c) an R1↔R3/R4 contradiction is caught and resolved (the
  Windows-no-sandbox vs "84% fewer prompts" O1 catch); (d) v1 is right-sized below the stated
  everything-scope. 26 untold requirements, 9 banned outcomes, ~30 sources (18 verified).

## Run log

| date | slug | sources | untold reqs | outcome |
|---|---|---|---|---|
| 2026-07-07 | claude-usage-os | ~30 found / 18 verified | 26 | mode: deep — PRD + seed shipped; R2 verify infra-blocked (salvaged+tagged); project reset 2026-07-09 |

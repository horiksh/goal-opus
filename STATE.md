# Project memory · goal-opus agent system

## Rehydration protocol
1. Read this file top to bottom (it is short by design; consolidation keeps it so).
2. Check `## Open failures` — resume any in-progress goal in `goals/` before starting
   new work.
3. Consult `## General rules` before re-deriving anything.
4. For goal runs, the procedure is `.claude/skills/goal-opus/SKILL.md` — read its
   `## Known failure modes` before Phase 1.

## Verified facts
- [2026-07-07] Skill frontmatter `model:` overrides the session model for inline skill
  turns; agent frontmatter `model:` overrides it for subagents. Verified against Claude
  Code docs (sub-agents.md, skills.md) during system design.
- [2026-07-07] A skill named `goal` would shadow the built-in `/goal` command — this
  system deliberately uses the name `goal-opus`.
- [2026-07-07] Agent definitions created in `.claude/agents/` mid-session are not
  IMMEDIATELY spawnable (`Agent type 'goal-maker' not found` right after creation) —
  but the registry CAN refresh later in the same session: both registered agents ran
  the rubric-check goal successfully without a restart. Retry once before falling back.
- [2026-07-08] Claude Code PreToolUse hooks run before every tool call and can
  allow/deny/MODIFY it (3-0 verified vs official hooks docs) — the reason enforcement
  hooks are banned from the goal loop: a hook can veto work the locked rubric requires.
- [2026-07-08] Code-graph navigation scores 0.83 vs 0.92 for a grep/read explorer
  overall; graphs win only on structural queries (arxiv 2603.27277v1, 3-0 verified).
  Grep over live files has zero staleness — decisive for a self-rewriting loop.
- [2026-07-08] Ponytail's benchmark numbers are self-reported against a no-skill
  baseline, and the project's original headline benchmark was retracted as inflated
  (its own benchmarks file, 3-0 verified). Star-count/ecosystem framing unconfirmed.

## General rules
- Define "done" as an executable, Default-FAIL rubric BEFORE any making. A criterion
  without an executable `verify` method is not a criterion.
- Evidence means a command output or file pointer, never "looks done."

## Key decisions log
- **D1** [2026-07-07] Maker AND verifier both run on `claude-opus-4-8` — explicit user
  decision, overriding the context pack's cheaper-grader default (docs/context/08).
  Verifier independence comes from fresh context + read-only tooling, not model tier.
- **D2** [2026-07-07] Installed project-level (this repo) rather than `~/.claude`, so
  every self-edit of the skill is a reviewable git diff. Promotion to user level is an
  M2 step, gated on: (1) one clean fresh-session run with registered agents, (2) one
  real multi-iteration goal, (3) ≥2–3 Eval suite entries. Promotion mechanism: NTFS
  **junctions** from `~/.claude/skills/<name>` to this repo's skill dirs (never copies —
  copies fork the self-editing skill); agent .md files may be plain copies (they don't
  self-edit). Post-promotion regression check: re-run the Eval suite goals.
- **D3** [2026-07-07] Write-back enforcement is a mandatory protocol phase (Phase 6) at
  M0; Stop-hook enforcement deferred to M1 (Windows hook scripting gets its own tested
  step).
- **D4** [2026-07-07] PRD generation is a command (`/prd`), not a plan-mode flow — plan
  mode can't be scripted/forced from a skill and blocks file writes; the same guarantee
  ("think before code") is achieved by the skill's hard documents-only rule. `/prd`
  seeds `criteria.seed.json` so `/goal-opus` executes what the PRD defined.
- **D5** [2026-07-07] One agent home, many build TARGETs — do NOT clone this repo per
  project (cloning forks the self-improving skill and splinters compounding). Every
  product-code goal declares a TARGET repo; product code + project STATE.md live there,
  system memory + run evidence live here. Raised by the user as a drift concern;
  adopted as a scope rule in both skills.
- **D6** [2026-07-07, revised same day] Research depth: `/prd` defaults to the 3-agent
  fan-out but MAY escalate to deep-research by its own judgment (domain stakes,
  conflicting sources, months-long investment), stating the choice in its report;
  `/deep-prd` FORCES the deep-research workflow (typing the command is the workflow
  opt-in), loud failure if the plugin is absent. The wrapper is a thin dispatcher
  holding no memory — all write-back stays in prd/SKILL.md (single brain, per D5).
- **D8** [2026-07-08] Tooling-augmentation verdicts (evidence:
  `docs/research/2026-07-08-tooling-augmentation.md`):
  **ADOPT** — Ponytail's decision ladder DISTILLED into goal-maker RULES + a
  completeness counter-guard + an over/under-engineering verifier lens; the plugin and
  its hooks REJECTED (PreToolUse hooks can deny/rewrite maker tool calls → collides
  with the locked-rubric loop; its headline benchmarks are self-reported and the
  original was retracted). **KEEP/DEFEND** — grep/Glob/Read over live files as the
  retrieval layer; REJECT embedding/RAG (Anthropic itself abandoned RAG in Claude Code
  for agentic search) and persistent maker-side code-graphs (staleness under a
  self-rewriting loop; graph 0.83 < grep 0.92 overall, graphs win only structural
  queries); single exception: verifier-only one-shot graph, gated on demonstrated
  token-bleed on structural criteria. **PILOT** — Obsidian as a HUMAN-ONLY read-only
  dashboard over memory (git the sole sync; cloud sync under agent writes produces
  conflict-file storms); agent-side Obsidian REJECTED (MCP-last). **Dreaming**: the
  pattern already exists as Phase 6 write-back; a separate cron tool is a
  non-deterministic duplicate — rejected.
- **D7** [2026-07-08] UI/UX pipeline: design direction comes EARLY (interactive
  `/design-direction` session with the user's live taste → frozen
  `docs/design/design-direction.md` + reference images + BV-list in the TARGET), then
  UI ships as vertical slices inside /goal-opus phases under **vision-verify**: maker
  and verifier both re-capture scripted screenshots; the verifier judges by Reading the
  images against references/baselines/BV-list (mechanically real — Read renders
  images); baselines promoted only by the orchestrator on accepted passes. Rejected
  alternatives: design-after-backend (UI-driven backend needs arrive too late — the
  usage-os PRD's U9/U10 proved it; that PRD was reset 2026-07-09, evidence in git
  history) and unanchored goal-loop UI (converges on functional-generic). Motion/interactive feel stays human-judged at slice demos.

## Open failures
_(none — the abort-probe entry closed 2026-07-07: abort path verified and reported;
workdir `goals/2026-07-07-abort-probe/` retained as evidence)_

## Lessons learned
- [2026-07-07] Infrastructure the loop depends on (agent definitions, skills, hooks)
  must exist BEFORE the session that uses it — E2E-test loops from a fresh session,
  never the session that scaffolded them.
- [2026-07-08] Ad-hoc research prompts must contain the persist-and-commit step AS PART
  OF THE TASK ("write the report to <path>, then commit"), not as advice around it —
  the tooling research session finished without writing its report; it took a
  cross-session nudge to recover the write-back. (/prd and /deep-prd already enforce
  this via Phase 7; the gap is only in hand-written prompts.)
- [2026-07-07] Deep-research (the workflow) is token-heavy (~2–5M/run, 100+ agents) and
  trips a ROLLING account session limit whose reset moves later with each big run. Recovery
  that works: read the task `.output` file (search/fetch/extract usually survive → salvage
  `result.confirmed`/`result.unverified` with their source URLs), RESUME from `runId` to re-run
  only verify/synthesize from cache, and run R3/R4 as SINGLE agents (small draw, succeed while
  the account is burst-limited). Re-firing the whole workflow is the wrong move — it wastes
  millions of tokens and extends the lockout. Full detail in `prd/SKILL.md` Known failure modes.
- [2026-07-07] When automated verification is infra-blocked, honesty preserves the contract:
  tag salvaged claims by true status (`[VERIFIED+SRC*]` = primary-source-extracted-but-vote-
  pending, `[REPORTED]` = single user report) and say so in the PRD provenance header. That is
  NOT the silent downgrade `/deep-prd` forbids; a silent swap to the cheap fan-out would be.
- [2026-07-09] Deep-research recovery, refined (extends the 2026-07-07 rolling-limit lesson):
  (1) the rolling session limit needs REAL IDLE HOURS to clear, not just the reset timestamp to
  pass — resuming within ~1–2h of a nominal reset re-tripped it three times; the resume that fully
  verified ran ~5h after the reset with the account otherwise idle. (2) `resumeFromRunId` replays
  every completed search/fetch/verify agent from cache for FREE — the full-verify resume cost 59k
  tokens vs ~2M cold. (3) The `deep-research` synthesize agent can THROW `StructuredOutput retry
  cap (5) exceeded` on a large confirmed-claim set, and the throw propagates past the script's own
  `if(!report){…salvage…}` guard — wrap the synthesize `agent()` call in try/catch so the salvage
  return fires. R1 reached 22/25 verified only after the try/catch patch + a rested-window resume.

## Last session
- [2026-07-07] Scaffolded the /goal-opus system and ran E2E verification. Run 1
  (wordfreq): success in 1 iteration — full make→verify→gate→write-back cycle
  exercised; hill-climb baseline = 1 iteration. Maker/verifier ran as general-purpose
  fallbacks on Opus (registered agents need a fresh session — see Lessons learned).
  Next: from a FRESH session, run /goal-opus once to confirm registered-agent routing
  (goal-maker/goal-verifier resolve, verifier tool allowlist enforced).
- [2026-07-07] Run 2 (abort-probe): aborted at bound=1 as designed — maker reported the
  impossibility honestly (no tampering, no thrash), verifier failed C1 with refutation
  evidence, write-back ran on the abort path. Abort machinery verified.
- [2026-07-07] Added `/prd` (research-first PRD generator, documents-only): three-agent
  research fan-out (best practices / analogs / untold-requirements mining) + adversarial
  gap check + PRD synthesis + criteria.seed.json handoff to /goal-opus. Not yet
  exercised on a real product statement — first real /prd run is the E2E test.
- [2026-07-07] Adopted home-vs-target separation (D5): goals now declare a TARGET;
  scope rules added to both skills, invariant added to CLAUDE.md, anti-pattern recorded
  in goal-opus. The wordfreq artifact in `tools/` predates this rule — treat it as
  probe residue, not a precedent.
- [2026-07-07] REGISTERED-agent routing confirmed (closes the fresh-session item):
  goal-maker and goal-verifier resolved from `.claude/agents/` and ran the rubric-check
  goal end-to-end (success, 1 iteration); wordfreq eval-suite re-run after the scope
  edits: PASS. New system tool: `tools/rubric_check.py` (use at Phase 1 sign-off).
  Promotion gate (D2): (1) registered-agent run ✔; (2) real multi-iteration goal —
  still pending; (3) Eval suite has 2 entries ✔.
- [2026-07-07] Added `/deep-prd` (thin dispatcher, D6): forces the deep-research
  workflow for Phase 2; `/prd` unchanged. Not yet exercised — needs a fresh session
  for the skill to register, plus the deep-research plugin present.
- [2026-07-08] Built the UI/UX layer (D7): vision-verify wired into goal-opus (Phase
  1/2/3 + a `## Vision-verify` section; verifier re-captures and judges by Reading
  images; baseline promotion orchestrator-only) and a new `/design-direction` skill +
  enforceable template (BV-list folds into rubrics verbatim). NOT yet E2E-tested — the
  first UI slice of a future project is the E2E test: check the verifier's verdict names
  the image files it viewed, and that a BV violation actually fails the run.
- [2026-07-08] Tooling research report landed (`docs/research/
  2026-07-08-tooling-augmentation.md`; the research session committed it after a
  cross-session nudge — see Lessons learned). Verdicts folded as D8 + three Verified
  facts.
- [2026-07-08] D8 Goals 1 and 3 EXECUTED, both success in 1 iteration: decision ladder
  + completeness counter-guard + over/under-engineering lens are live in the loop
  (Goal 3's run proved it — its maker returned the completeness enumeration and its
  verifier applied the lens unprompted); primitives-first retrieval invariant codified
  (CLAUDE.md bullet + docs/context/11-retrieval-invariant.md + /prd loop-retrieval
  guard). Goal 2 (Obsidian dashboard) DECLINED by the user — do not re-stage it.
  Known stale ref: CLAUDE.md line 5 + pack README still say "files 01–10"; file 11 now
  exists (left alone for the 6-line cap; fix opportunistically).
- [2026-07-09] PROJECT RESET at the user's request: deleted
  `prds/2026-07-07-claude-usage-os/` (Claude Mission Control, the first real `/deep-prd`
  run) — the repo now has NO projects; the user is restarting from 0 after a repo
  revision. Do not resume anything usage-os-related. What survives: the `/deep-prd`
  protocol validation itself (full run exercised 2026-07-07, R4 catches confirmed), the
  deep-research rate-limit recovery lessons above, and the prd skill's eval-suite/run-log
  entries (marked historical). Artifacts recoverable from git history (commit 77487f0
  on the LOCAL `private-history` branch — see the publishing entry below).
- [2026-07-09] REPO PUBLISHED: public at https://github.com/horiksh/goal-opus (MIT,
  README added). Branch model: `main` = public, fresh root (single "Initial public
  release" commit, noreply author); `private-history` = the full pre-release history,
  LOCAL ONLY — never push it (it contains the reset usage-os PRD and personal-email
  commit metadata). Day-to-day work happens on `main`; pre-release commit hashes cited
  in this file resolve only on `private-history`.
- [2026-07-09→11] `/deep-prd "an agentic OS for this repository setup"` — first real PRD run since
  the 07-09 reset. Scope locked with the user (4 Qs): PORTABLE Claude-Code-native framework · solo
  operator first · Windows/Claude-Code v1 runtime · runnable orchestration layer as v1 "done".
  MID-FLIGHT (not a completed run): R1 (best practices) FULLY VERIFIED 22/25 after four
  rate-limited attempts + a script-patched rested-window resume → `prds/2026-07-09-agentic-os/
  research/R1-best-practices.md`; R2 (analogs + failure modes) SALVAGED 12 verified + 13 reported
  (verify was limit-truncated) → `research/R2-analogs.md`. PENDING: R3 (untold reqs), R4 (gap
  check), PRD.md synthesis, criteria.seed.json, final Phase 6/7. A WIP PR was opened for the
  research phase. Key R1 finding: the external primary-source evidence VALIDATES this repo's own
  design (maker≠grader, Default-FAIL rubric, plain-file cross-session state, primitives-first
  retrieval) — the product is largely *packaging what's already validated* into a portable
  framework. Resume pointer: run R3 (single agent) over R1+R2, then R4, then synthesize the PRD +
  seed. Slug date 07-09 = run start; session spanned to 07-11 due to the rate-limit waits.
- [2026-07-09→11] `/deep-prd` agentic-os now COMPLETE (supersedes the mid-flight note above). R3
  (32 untold reqs, U1–U32) + R4 (adversarial gap check) ran as single agents (survived the limit).
  R4 caught the highest-severity gap — the product's OWN orchestrator control loop had no research,
  only its sub-parts did — plus `[REPORTED]`-only confidence clusters and 7 contradictions; ALL folded
  back into synthesis (§4d flags the control loop as design-composed-from-verified-primitives; every
  requirement carries a [V]/[R]/[A]/[D] confidence tier; each contradiction resolved by an explicit v1
  scope decision — single-target, single-threaded, local `/loop`, Windows-first-with-copy-fallback,
  manual-consolidation). Shipped `prds/2026-07-09-agentic-os/PRD.md` + `criteria.seed.json` (5 stated,
  36 untold, 11 banned, 12 seeded criteria; rubric_check PASS). Landed on PR #1
  (github.com/horiksh/goal-opus/pull/1). NEXT: `/goal-opus` at **P0 (Bootstrap & install)** against a
  chosen TARGET. Eval-suite + Run-log entries added to prd/SKILL.md.

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
- [2026-07-12] NTFS directory junctions are creatable on this Windows box WITHOUT
  elevation in user/project/temp dirs — agentic-os P0 install created goal-opus skill
  junctions (pwsh `LinkType=Junction`, `fsutil reparsepoint query` exit 0) and the copy
  fallback (`AGENTIC_OS_NO_JUNCTION=1`) produced a byte-identical (sha256-matched) copy.
  De-risks the PRD's U24/U25 §9 assumption ("junctions need privilege and can fail").
  Also verified: removing a junction via `rmdir`/`os.rmdir` does NOT follow the link to
  delete the canonical payload source — round-trip install→uninstall is source-safe.

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
- **D9** [2026-07-12] The agentic-os PRODUCT lives in its own TARGET repo
  `D:\horil\agentic-os` (fresh, git base 31ddc40), NEVER the home — enforces B1/D5
  (product ≠ home; verified BP1-clean this run). Payload model = **self-contained
  framework**: agentic-os vendors its OWN copy of the goal-opus skill/agents/tools/
  templates and installs THAT (portable, fresh-clone, no runtime dep on the home), per
  PRD S1. Known tension (accepted for v1): the vendored goal-opus copy can drift from
  the home's self-editing skill; a home→framework sync mechanism is deferred to a later
  phase, not P0. User-signed both decisions at Phase 0.

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
- [2026-07-12] Rubric-design pattern for INTEGRATION-HEAVY phases (where the real behavior drives a
  non-deterministic LLM and so can't be a rubric `verify`): make the CONTROL FLOW verifiable by
  (1) MANDATING a deterministic mock/test handle in the rubric spec itself — a documented env/flag +
  fixture schema the maker MUST implement (e.g. `AGENTIC_OS_MOCK_RUNNER=<fixture.json>`), so every
  criterion is executable offline against the loop's OWN outputs (states/budgets/logs/checkpoints)
  while only the dependency's content is faked; AND (2) adding a BANNED OUTCOME that the real
  (non-mock) path must EXIST and be the DEFAULT — else you ship a mock-only fake that passes
  control-flow tests with no real integration. Proven on agentic-os P1: 8/8 criteria graded
  deterministically; the guard (BP8) confirmed the real path is default and genuinely invokes
  `claude`. Reuse this shape for any phase whose real work is non-deterministic (e.g. P2 crash-resume).
- [2026-07-13] **FAKE-STUB-OF-THE-REAL-DEPENDENCY is the deterministic-but-FAITHFUL test substrate**
  (the resolution to MOCK-VERIFIED≠LIVE-READY). A pure mock hides the real dependency's output shape,
  edge bytes, and side effects. Instead build a STUB of the real dependency that (a) emits its TRUE
  output format (agentic-os P9's fake-`claude` stub emits a real `claude -p --output-format json`
  envelope — real key set, markdown-fenced `result`), (b) carries the EDGE CONDITIONS that bite live
  (NON-ASCII bytes → the cp932 decode crash), and (c) produces the REAL SIDE EFFECTS (creates an actual
  product file → exercises checkpoint-staging + undo). Placed on a temp PATH as the real binary's name,
  it drives the REAL adapter path deterministically (no tokens, no live nondeterminism) yet reproduces
  exactly what the pure mock hid — P9 fixed 5 live-§8 bugs this way and the verifier re-ran them on its
  OWN stub. GENERAL RULE: for any real-dependency adapter, ship a faithful stub (true format + edge
  data + real side effects), not just a value mock.
- [2026-07-13] **MOCK-VERIFIED ≠ LIVE-READY (the flip side of the lesson above).** All of agentic-os
  P0–P4 passed via the deterministic mock, yet the FIRST live run (§8) proved the REAL runner is
  broken against real `claude -p --output-format json`: the CLI returns an ENVELOPE
  (`{type,subtype,result:"<the agent's JSON report as a STRING>",usage:{input_tokens,output_tokens,
  cache_*}}`), but `_parse_last_json` returns that envelope AS the maker report, so
  `files_changed`/`evidence`/`overall` read empty (no real goal can pass) and `_usage_tokens` reads a
  `total_tokens` key the envelope lacks (→0). GENERAL RULE: a deterministic mock is a CONTROL-FLOW
  harness, never evidence the real dependency works — the mock's very determinism HIDES the real
  tool's output-format/permission/parsing surface. The live acceptance run against the REAL tool's
  actual output is MANDATORY before "done"; a banned-outcome guard that the real path merely EXISTS
  and is default (agentic-os BP8) is necessary but NOT sufficient — it proves the path is wired, not
  that it parses reality. Confirmed for ~$0.05 with one `claude -p` probe rather than a doomed full run.
- [2026-07-15] **For a PRD about a UI/observer over an EXISTING codebase, add a CODE-VERIFICATION pass between R3/R4 and
  synthesis — the producer's data model is VERIFIABLE, not assumable.** On the agentic-os-ui PRD, R3 honestly flagged its
  own "verification backlog" (torn reads? atomic writes? crash-marker semantics? scrub coverage? lock/CAS?) as
  [ASSUMPTION]s it couldn't check. The main loop grepped/read the live CLI (`agentic-os/cli/agentic_os.py`) in minutes
  and upgraded FIVE claims [A]->[V]: run-status.json is written IN PLACE non-atomically (torn reads are REAL, not
  hypothetical -> the UI's torn-read handling is a hard MUST + a 3-line producer fix recommended); in_flight/queue-consumed/
  notify-events are all real; and NO lock/lease/CAS exists (so UI control is net-new coordination). This ALSO resolved R4's
  single "architecture-impossible" flag (per-iteration replay): run-status.json is a snapshot, but run-log.jsonl is the
  durable per-iteration journal (the CLI already has `_rebuild_progress_from_runlog`). GENERAL RULE: when the product
  observes/controls an existing system, verify its data-model claims against the code before locking the PRD.
- [2026-07-15] **When the user leaves scope questions unanswered, tie each [ASSUMPTION] to a concrete downstream GATE, not
  just the Risks section.** The agentic-os-ui user didn't answer the 4 scope Qs; proceeding autonomously with defaults is
  correct (per /prd Phase 1), but the improvement is anchoring each assumption to WHERE it gets verified (here: the U0
  `/design-direction` session is the named checkpoint for A1 delivery / A2 control-scope / A3 fleet-scope / A4 ambition).
  An assumption with a verification GATE is actionable; one merely "logged in Risks" is inert.

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
- [2026-07-12] `/goal-opus` **P0 (Bootstrap & install)** — SUCCESS in **1 iteration** (first real
  product-code goal against a SEPARATE TARGET). TARGET = `D:\horil\agentic-os` (new repo); payload =
  self-contained framework (D9). Built + committed there (`9aeb876`): dual-shell (PowerShell+Git-Bash)
  `init`/`install`/`uninstall`/`upgrade` CLI, git-precondition, preflight + schema-version, and an
  NTFS-junction-with-copy-fallback install mechanic driven by a relative-path manifest; vendored
  goal-opus payload; `tests/test_p0.py` 53/53. goal-verifier PASS on all 8 criteria (CP1–CP8) + all 6
  banned outcomes clear, each re-run independently on fresh throwaway repos
  (`goals/2026-07-12-p0-bootstrap-install/reports/iter-1.json`). Home stayed clean (BP1 — only run
  evidence landed here). Promotion gate D2 item (2) "one real **multi-iteration** goal" is STILL
  pending — this converged in 1. NEXT: `/goal-opus` **P1 (Orchestrator control loop, §4d)** against the
  same TARGET, scoping the C1/C3/C6/C7 + U3/U11/U12/U13/U15/U34 subset.
- [2026-07-12] Target repo PUBLISHED **private** at https://github.com/horiksh/agentic-os (default
  `main`, MIT, noreply git config). Distinct from the public home repo (github.com/horiksh/goal-opus).
  Caveat recorded in the target's own STATE.md: its first 3 commits carry a personal gmail address
  (pre-dated the config fix) — harmless while private; rewrite to noreply before any public flip.
- [2026-07-12] `/goal-opus` **P1 (Orchestrator control loop, §4d)** — SUCCESS in **1 iteration**
  (bigger, harder build than P0: 240k maker tokens, 82 self-tests — still first-try). Extended the P0
  CLI in `D:\horil\agentic-os` (commit `5bcb358`): the §4d per-iteration loop (poll sentinels → check
  budgets → pick → gate rubric → run one goal-opus iteration → gate → write back), run-lifecycle state
  machine, `AGENT_STOP`/`STEER.md` sentinels, per-goal + aggregate-iteration + token budgets (no-budget
  refusal), no-progress detector, empty-queue idle exit, verb surface (+ `resume`/`undo` stubs), a
  deterministic mock runner (`AGENTIC_OS_MOCK_RUNNER`) and the DEFAULT real goal-opus integration.
  goal-verifier PASS on all 8 criteria (QP1–QP8) + 8 banned outcomes, each re-run on fresh throwaway
  repos (`goals/2026-07-12-p1-orchestrator-control-loop/reports/iter-1.json`); tests 82/82 P1 + 53/53 P0.
  Home clean (BP1). Promotion gate D2 item (2) "one real **multi-iteration** goal" is STILL pending —
  both P0 and P1 converged in 1. NEXT: `/goal-opus` **P2 (Durable memory & write-back)** — crash/cancel
  write-back guarantee, idempotent resume from checkpoint + run log, export, secret-scrub, size-warning
  (scopes master-seed C2/C4/C8 + reqs U5/U6/U7/U10/U21/U30/U31/U32).
- [2026-07-12] `/goal-opus` **P2 (Durable memory & write-back)** — SUCCESS in **1 iteration**.
  Extended the P1 orchestrator in `D:\horil\agentic-os` (commit `7d943fe`, FRAMEWORK_VERSION 0.3.0):
  incremental idempotent journaling (fsync'd `iter_begin` + `in_flight` crash marker before each step),
  a real crash-durable `resume` (replacing the P1 stub) with idempotent replay keyed by
  `(goal,iter,state)` via a `writeback-ledger.json` + duplicate-proof STATE.md rows, a pre-write secret
  scrub + at-rest `scrub` verb, an `export` backup, and a `status` size-threshold WARNING. Mock gained
  `crash_after_iteration` + `note`. goal-verifier PASS on all 7 criteria (RP1–RP7) + 7 banned outcomes,
  each re-run on fresh throwaway repos it crashed itself (forced a double-resume; blocked all sockets
  during export) — `goals/2026-07-12-p2-durable-memory-writeback/reports/iter-1.json`; tests 64/64 P2 +
  82/82 P1 + 53/53 P0. Home clean (BP1). Promotion-gate D2 item (2) "one real **multi-iteration** goal"
  is STILL pending — P0, P1, and P2 all converged in 1 (three substantial phases, zero re-iterations;
  worth watching whether rubrics are adversarial enough, though the mock-runner substrate + tight
  scoping plausibly explain the clean convergence). NEXT: `/goal-opus` **P3 (Safe autonomy)** —
  rollback/undo + optional approve-before-land gate, least-privilege allowlists, classifier-decline
  branch (scopes master-seed C9/C10 + reqs U22/U23/U33; `undo` is still a stub until then).
- [2026-07-12] `/goal-opus` **P3 (Safe autonomy)** — SUCCESS in **1 iteration**. Extended the P2
  orchestrator in `D:\horil\agentic-os` (commit `3148662`, FRAMEWORK_VERSION 0.4.0): a real `undo`/
  rollback (undo pointer = pre-change SHA, BP7-safe dirty-tree refusal, reflog-recoverable — replacing
  the P2 stub), an evidence-checking land-gate that flags a gamed pass (`gamed_pass` mock affordance),
  an optional `--approve-before-land` toggle + `approve` verb, a classifier-decline fallback branch
  (routing event, never retried), and env-gated least-privilege (no blind `--dangerously-skip-
  permissions`; verifier stays read-only). goal-verifier PASS on all 5 criteria (SP1–SP5) + 7 banned
  outcomes, re-run on fresh throwaway repos it landed/gamed/**dirtied**/undid itself — BP7 verified by
  a dirty-tree undo that refused with user work intact — `goals/2026-07-12-p3-safe-autonomy/reports/
  iter-1.json`; tests 64/64 P3 + 64/64 P2 + 82/82 P1 + 53/53 P0. Home clean (BP1). **Four phases
  (P0–P3), four first-try 1-iteration passes** — promotion-gate D2 item (2) "one real MULTI-iteration
  goal" is STILL unmet; the verifier genuinely refuted each and found nothing, so this reads as real
  quality (tight scoping + mock substrate), not weak rubrics. NEXT: `/goal-opus` **P4 (Observability
  & notification)** — tailable run-status polish + minimal push notify (master-seed C-none-new + reqs
  U9/U35); then §8 FINAL ACCEPTANCE (the LIVE end-to-end run every phase deferred).
- [2026-07-12] `/goal-opus` **P4 (Observability & notification)** — SUCCESS in **1 iteration**.
  Extended the P3 orchestrator in `D:\horil\agentic-os` (commit `fc8200e`, FRAMEWORK_VERSION 0.5.0):
  a tailable per-iteration `run-status.json` + a compact one-line `status` glance + bounded
  `status --follow`, and a push-notify hook (`AGENTIC_OS_NOTIFY_CMD`) fired once per
  finish/block/budget/decline — optional, non-fatal, local, secret-scrubbed (payload through the P2
  scrub). goal-verifier PASS on all 4 criteria (OP1–OP4) + 7 banned outcomes, re-run on throwaway
  repos (it crash-captured an intermediate status to prove live writes, forced a nonzero-exit hook,
  routed a secret) — `goals/2026-07-12-p4-observability-notification/reports/iter-1.json`; tests 61/61
  P4 + P0/P1/P2/P3 unchanged. Home clean (BP1). **v1 CORE (P0–P4) COMPLETE — five phases, five
  first-try 1-iteration passes.** Promotion-gate D2 item (2) "one real MULTI-iteration goal" remains
  unmet across the whole build. NEXT: **§8 FINAL ACCEPTANCE** — the LIVE end-to-end run (`agentic-os
  run` driving real goal-opus loops with `claude` on PATH, ≥2 goals, bounded/steerable/resumable/
  reversible), verified two ways. Inherently non-deterministic (real LLM) → a demo/acceptance run,
  NOT a mock-graded goal-opus phase — the one thing every phase deferred. P5+ (cloud, concurrency,
  dreaming, multi-target, cross-platform, adopter docs) → future PRDs.
- [2026-07-13] **§8 FINAL ACCEPTANCE attempted → FAILED (as built, §8 cannot pass).** `claude` found at
  `C:\Users\horil\.local\bin\claude.exe` (not on PATH; added for the attempt). Install + enqueue-2 +
  the real-run refusal-without-claude all work; the LIVE loop does NOT — a cheap `claude -p
  --output-format json` probe confirmed the real runner's live-integration bugs (see Lessons learned
  2026-07-13): (1) `_invoke_claude`/`_parse_last_json` return the CLI's result ENVELOPE, not the agent
  report nested in `result` → maker/verifier reports unreadable → every real goal aborts; (2)
  `_usage_tokens` reads `total_tokens` (absent from the envelope) → token budget reads 0; (3) the
  headless maker needs the `AGENTIC_OS_DANGEROUSLY_SKIP_PERMISSIONS` opt-in (or a settings allowlist)
  to write files. Also a minor finding: the real run journals `iter_begin`/`in_flight` BEFORE it checks
  `which(claude)`, leaving a stale `state=running` on a claude-less run (wants a run-start preflight).
  These are recorded as Open failures in the TARGET STATE.md. NEXT (recommended): a **P8 real-runner-
  hardening** /goal-opus goal (unwrap the envelope → parse the inner report; fix `_usage_tokens`;
  run-start claude preflight; document the permission opt-in for live runs) THEN re-run real §8. This
  is the self-improving loop WORKING: five mock-green phases, and the live probe caught the real gap.
- [2026-07-13] `/goal-opus` **P8 (real-runner hardening)** — SUCCESS in **1 iteration** (the fix born
  from the §8 finding). Committed in `D:\horil\agentic-os` (`671c82a`): `_extract_agent_report` unwraps
  the `claude -p --output-format json` envelope + parses the markdown-fenced report in `result`;
  `_usage_tokens` sums envelope `input_tokens+output_tokens`; `cmd_run` preflights `which(claude)`
  before journaling; docs state the live-run write opt-in. Verified deterministically against a REAL
  captured envelope — and the goal-verifier **re-captured its own fresh envelope** to defeat a
  hand-built fixture (BP2) — `goals/2026-07-13-p8-real-runner-hardening/reports/iter-1.json`; test_p8
  30/30, P0–P4 unchanged. Sign-off wasn't returned so I proceeded unattended per protocol (recorded in
  GOAL.md). The §8 blocker is now RESOLVED in the target's Open failures.
- [2026-07-13] **LIVE §8 CORE PASSES — the P8 fix validated end-to-end against real `claude`.** A bounded
  one-goal live run (sandboxed throwaway repo, `AGENTIC_OS_DANGEROUSLY_SKIP_PERMISSIONS=1`) went
  `session_start → goal_start → iteration(verdict=success, changed=True, tokens=2020) → land_gate=land →
  goal_end(success) → session_end(success)`: the LIVE maker wrote `greet.txt='hello'`, the LIVE verifier
  graded PASS, the gate landed it, and it wrote back a real git checkpoint (`88e85f5`) with real token
  accounting — all of which were broken pre-P8. Evidence:
  `goals/2026-07-13-p8-real-runner-hardening/reports/live-s8-smoke/`. This closes the critical §8
  uncertainty (does the live loop actually work — YES). REMAINING for a FULL §8 acceptance: the ≥2-goal
  sequence + LIVE `AGENT_STOP`/`resume`/`undo` + the two-way verification — a larger (still cheap: ~2k
  tokens/goal) live exercise, offered to the user. Cost so far: one probe + captures + one 2020-token
  live goal (~$0.1 total). NOTE: this live run is finally a real end-to-end integration (though still
  1-iteration); promotion-gate D2 item (2) "one real multi-iteration goal" remains technically unmet.
- [2026-07-13] **FULL live §8 RAN → does NOT pass. It surfaced a CLUSTER of 5 real integration bugs,
  ALL mock-hidden** (the strongest possible proof of the MOCK-VERIFIED≠LIVE-READY lesson: 5 phases + a
  fix + an ASCII smoke all green, yet the full live run has 5 bugs). WORKED live: real g1 core + the LIVE
  AGENT_STOP mid-run halt (g1 landed, g2 never started, state=stopped — the kill-switch works with the
  real runner). BUGS (detail: target Open failures + `goals/2026-07-13-p8-real-runner-hardening/reports/
  live-s8-full/FINDINGS.md`): (1) [high] every `subprocess.run(text=True)` lacks `encoding="utf-8"` →
  cp932 (this Japanese-locale box) crashes on non-ASCII claude/git output; (2) [high] the checkpoint
  stages only STATE.md + `.agentic-os/`, NOT the maker's product files → `undo` can't revert real
  autonomous changes (untracked); (3) [med] queue not consumed (`run` re-runs completed goals); (4) [med]
  `resume` no-ops after an AGENT_STOP halt; (5) [low] no None-guard on a failed-decode report. Both P8's
  fix AND every mock phase were green — only the live acceptance caught these. NEXT (recommended): a
  focused **P9 live-hardening** /goal-opus goal (fix 1–5, load-bearing 1+2, ground the tests in a
  cp932-locale + real-untracked-file scenario), then re-run full live §8. This is the loop doing its
  job — do NOT mark v1 "done" until the full live §8 passes.
- [2026-07-13] `/goal-opus` **P9 (live-hardening)** — SUCCESS in **1 iteration**. Fixed all 5 live-§8
  bugs in `D:\horil\agentic-os` (commit `f2c9308`, FRAMEWORK_VERSION 0.6.0): (1) `encoding="utf-8",
  errors="replace"` on all 11 `subprocess.run(text=True)` (cp932 crash gone); (2) checkpoint now stages
  the maker's reported `files_changed` so `undo` reverts a real created file — while still refusing over
  UNreported user work (BP4/BP7 intact); (3) queue consumption (completed goals marked `consumed`);
  (4) `resume` continues after an AGENT_STOP halt (documented); (5) clean OrchestratorError on empty/
  garbage claude output. Verified via a FAITHFUL fake-`claude` stub (see Lessons learned 2026-07-13) —
  the verifier wrote its OWN stub and drove the real runner under cp932 to confirm the fix is
  load-bearing. `goals/2026-07-13-p9-live-hardening/reports/iter-1.json`; test_p9 54/54, P0–P4/P8
  unchanged. NEXT (in progress): **re-run the FULL live §8** — the real acceptance the P9 fixes enable.
- [2026-07-13/15] **FULL LIVE §8 PASSES — v1 agentic-os is DONE.** After P9, the full §8 acceptance ran
  end-to-end against real `claude`: install+bootstrap → enqueue 2 → run both goal-opus loops (real
  maker→verifier→gate→write-back, 4337 real tokens, 2 checkpoints) → **live AGENT_STOP** halted within
  one iteration (g1 landed, g2 not started) → **`resume`** continued g2 without redoing g1 → **`undo`**
  reverted the last landed change (beta.txt gone, alpha.txt kept, HEAD→g2's pre-change SHA, reflog-
  recoverable). Verified TWO WAYS: (a) replay from status+git reproduces the state; (b) a FRESH-CONTEXT
  goal-verifier confirmed all 5 §8 claims from artifacts ALONE (overall PASS) — it recovered the
  pre-undo run-log from the g2 checkpoint's committed blob. Evidence:
  `goals/2026-07-13-p9-live-hardening/reports/full-s8-pass/VERDICT.md`. **The whole arc closed:
  P0–P4 mock-green → §8 live probe caught a broken adapter → P8 fixed parsing (live core passed) →
  full §8 caught 5 more mock-hidden bugs → P9 fixed them (faithful fake-claude stub) → full live §8
  PASSES two ways.** That IS the self-improving loop's thesis, demonstrated end-to-end: independent
  live verification kept catching what green mocks hid, until the real thing actually worked. D2 item
  (2) "one real multi-iteration goal" is satisfied in SPIRIT (the loop iterated across P8/P9 to fix real
  bugs), though each goal-opus phase itself still converged in 1. v1 remaining scope is only P5+
  (cloud/concurrency/dreaming/multi-target/cross-platform/adopter-docs) → future PRDs.
- [2026-07-15] `/prd "cutting-edge UI/UX for the agentic-os"` — first /prd against the now-DONE agentic-os engine (the
  UI observes/controls it). Mode: standard 3-agent fan-out (NOT deep-research — observability-dashboard domain is
  well-trodden with dense analogs; a local single-operator tool; deep-research's rate-limit failure mode not worth it)
  + single-agent R4 gap-check + single-agent R5 gap-closer. User did NOT answer the 4 scope Qs → proceeded autonomously
  with defaults logged as [ASSUMPTION] tied to the U0 /design-direction gate (A1 local web app · A2 phased full-control,
  read-only first · A3 single-target/many-goals · A4 daily-driver+visionary). R4 EARNED ITS KEEP (2nd time the
  "which promised capability has NO research" test caught the headline gap): the user's FIRST-named mechanic — SKILLS
  INSTALLED — had zero research, and "intuitive"/"visionary" were unbacked; spawned R5 to close them (Claude Code
  /plugins schema, NN/g onboarding, LangGraph live-loop-graph, functional-motion doctrine). Code-verified R3's data-model
  assumptions against the live CLI (5 claims [A]→[V]; resolved R4's per-iteration-replay flag via run-log.jsonl). Shipped
  `prds/2026-07-15-agentic-os-ui/PRD.md` (7 stated, 43 untold U1–U43, 14 banned B1–B14, ~34 sources) +
  `criteria.seed.json` (14 criteria C1–C14 + 14 banned; rubric_check PASS); copied PRD+seed into the TARGET
  `agentic-os/docs/` (UI-PRD.md, ui-criteria.seed.json). NEXT: `/design-direction` in `D:\horil\agentic-os` (U0, MANDATORY
  before any UI slice — vision-verify needs anchors), then `/goal-opus` at U1 (read-only observatory: loopback+Host-
  validation, torn-read-safe reader, 4 mechanics, staleness/crash/empty states, a11y baseline).

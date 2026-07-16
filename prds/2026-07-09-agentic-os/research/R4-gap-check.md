# R4 — Adversarial gap-check (VERIFIER posture)

> Refutation pass over the delivered research set (R1 verified · R2 salvage-mostly-`[REPORTED]` ·
> R3 untold-reqs U1–U32). Goal: prove the research is INCOMPLETE, not extend it. Judged the three
> notes AS DELIVERED (no external re-fetch). Verdicts: **REAL GAP → fix how** vs **acceptable
> deferral → why**. Severity ranking at the end.

---

## 1 · Missing requirement CATEGORIES

**1.1 — The orchestrator's OWN control loop / run-lifecycle state machine is never specified. [REAL GAP — highest]**
The product IS "a runnable orchestration layer." R3 enumerates run *states* — idle (U3), paused/
rate-limited (U4), no-progress (U15), success/abort, resume (U30), budget-stop (U12/U13) — but
**nothing specifies the loop that transitions between them**: how the orchestrator picks the next
goal, spawns goal-opus, polls sentinels each iteration, evaluates stop conditions, writes back, and
re-enters. R1 §1 documents a *single* builder/evaluator `while`-loop — NOT an orchestrator that
sequences *multiple* goal-opus runs over shared memory. So the central deliverable is decomposed
into guards and states but the state machine is never assembled, and no research describes the
orchestration layer above goal-opus at all. **PRD must:** specify the orchestrator control-flow /
lifecycle state machine (states + transitions + per-iteration poll order) as a first-class section;
flag that it has no direct research support (see §4.1).

**1.2 — Operator command/verb surface is scattered, never enumerated. [REAL GAP]**
`init` (U1), install/uninstall/upgrade (U26), scrub (U7), `/goal-opus`, `/prd`, `/loop` appear
piecemeal. There is no coherent spec of what the solo operator actually *types* to: start an
orchestrated run, enqueue a goal, check status, pause, resume, redirect. R1 gap #3 asks whether
tail/watch is the observability ceiling but never treats the operator's INPUT surface. **PRD must:**
define the command surface as its own section (the operator's verbs), even if minimal.

**1.3 — Rollback / undo of a bad-but-"passing" autonomous change. [REAL GAP — high severity]**
The system lands autonomous commits across many iterations, and R1 §3 + R2 Bucket 1 both say the
Default-FAIL gate is **prompt-level, NOT a security boundary** — the verifier can be "talked into
deciding [bugs] weren't a big deal." Yet the only recovery mechanisms are for *resuming* (U30
resume-from-checkpoint, U32 commit-on-stop), never for *reverting* a completed-but-wrong change.
No requirement covers review-before-merge, an undo/revert command, or a human approval gate before
autonomous changes reach a durable branch. For an autonomous system with an admittedly gameable
gate, the absence of an undo path is dangerous. **PRD must:** add a rollback/undo + optional
land-gate requirement (re-research the safe-autonomy pattern; do NOT scope this out silently).

**1.4 — Testing / eval of the OS ITSELF. [REAL GAP]**
The system's whole purpose is verifying other work, yet nothing in the set covers how the
orchestration layer is itself tested: regression suite, resumability actually resuming, a schema
migration (U8) not stranding a home, install/uninstall (U26) round-tripping. A self-*improving*
system with no self-test story regresses silently. **PRD must:** add a self-test/eval requirement
(smoke test of the run loop + migration + install lifecycle), or explicitly accept the regression
risk with a stated reason.

**1.5 — Multi-TARGET management. [REAL GAP, likely v1-deferrable — must name]**
Scope = "turn ANY git repo into a home" and CLAUDE.md = "product code lives in each goal's TARGET
repo," implying N targets. U2 gates git *per TARGET* but nothing covers a target registry,
switching targets, or isolating each target's memory/state from the HOME. **PRD must:** either
scope v1 to a single target explicitly, or add a target-management requirement — decide, don't
leave implicit.

**1.6 — Operator notification / alerting for long unattended loops. [REAL GAP]**
Primary user is a solo operator; a run can go hours and R3 covers only *pull* watchability (U9
status file, U11 sentinels). Nothing covers *push* — how the operator is alerted when the run
finishes, blocks, hits budget, or the model declines (U22). **PRD must:** add a minimal
notification requirement or explicitly defer with a reason.

**1.7 — Adopter onboarding/docs and licensing/distribution for a PUBLIC framework. [ABSENT — acceptable deferral, must scope]**
The repo shipped an "Initial public release," but the set has no adopter README/quickstart/
troubleshooting and no OSS license / contribution / release-versioning story. R1 covers the
plugin+marketplace *channel* and U26 the install *lifecycle*, not docs or licensing. **Deferral OK
because** v1 = solo operator, portability is a design constraint not a v1 gate — but the PRD must
explicitly scope these OUT rather than silently omit them.

**1.8 — Toolchain/environment preflight beyond git. [MINOR GAP]**
U2 checks git-repo; nothing checks the required Claude Code version (R1 warns version pins drift),
PowerShell/Git-Bash availability (U27), or plugin registry state before a run. **PRD should:** fold
a preflight check into U1 bootstrap.

---

## 2 · Unsourced / weakly-sourced claims (load-bearing, unverified support)

**Systemic finding first:** the ENTIRE set is near-monoculture Anthropic primary sources; R1's own
caveat admits "single-vendor," and its two benchmarked figures (90.2%; 4×/15×; 80% variance) are
**self-reported on an internal, now-superseded-model eval** — "verified" means "survived R1's
3-vote against an Anthropic source that grades itself." There is no independent corroboration of the
core harness spine. Separately, **many R3 requirements cite repo-internal docs (context-04,
context-08, STATE.md D2/D3) as if they were research** — those are not in the research set and R4
cannot verify them; a requirement whose only real support is an internal design doc is effectively
unsourced from the research. The PRD provenance header must carry both caveats.

Requirements whose **only** load-bearing support is unverified `[REPORTED]`, `[ASSUMPTION]`, or a
non-research repo doc:

- **U28 (scheduling posture)** — only `[REPORTED routines]`; R1 states plainly *no routines claim
  survived verification*. The single biggest gap vs the brief rests on zero verified evidence.
- **U31 (idempotent re-run)** — only `[REPORTED temporalio/rules]` + `[REPORTED vadim.blog]` (a
  personal blog). A core correctness property with no verified support.
- **U8 (schema version + migration)** — the version-drift citation is `[VERIFIED]` but is about
  `/goal` version *pins*, NOT schema migration; the actual migration requirement rests on
  `[REPORTED temporalio TMPRL1100]`. Load-bearing, unverified.
- **U16 (file-ownership partitioning)** — only `[REPORTED agent-teams]`.
- **U19 (decomposability check)** — only `[REPORTED building-c-compiler]`.
- **U12 (orchestrator global budget)** — only `[REPORTED ralph-wiggum]`.
- **U9 (tailable status file)** — only `[REPORTED disler]`, a single practitioner GitHub repo.
- **U29 (laptop-sleep durability)** — `[VERIFIED — talk] context-04` (a talk, not in the set) +
  `[REPORTED routines]`. No verifiable support.
- **U24 (NTFS-junction install mechanic)** — the plugin-packaging citation is `[VERIFIED]` but the
  junction-vs-copy mechanic is **R1's own gap #2, "NO surviving primary claim"** + `[ASSUMPTION]`.
- **U25 (config-merge precedence)** — cited `[VERIFIED]` fact is settings.json *pinning*; the actual
  precedence/override semantics are **R1 gap #2, "unresolved."**
- **U22 (decline detection + fallback)** — `harness-design` cited only for a "principle";
  substance = context-08 + `[ASSUMPTION]`. Essentially no direct research support.
- **U7 / U21 (secrets scrub / pre-write guard)** — substance rests on context-08 (repo doc);
  the harness-design citation covers only the file-as-message-bus *fact*.
- **U14 (single-thread-by-default fan-out gate)** — the *verified* leg (90.2%/15×) justifies "fan-out
  is expensive," but the *direction* (single-thread by default) leans on **Cognition "Don't Build
  Multi-Agents," a secondary blog below the verify cut.** The #6 highest-leverage architecture fork
  partly rests on unverified opinion.
- **U20 (prompt-injection posture)** — mis-mapped citation: the `[VERIFIED agent-teams]` claim is
  about *relayed approvals between teammates* being untrusted, NOT about *untrusted web/TARGET
  content* injection. The requirement is inferential; its verified citation addresses a different
  threat.

**PRD must:** attach a confidence tier to each requirement; downgrade the above to "provisional —
verify before build" or seed them as rubric criteria to be proven during the build; re-research U28,
U24/U25, U31 specifically (they are load-bearing AND unverified AND high-leverage).

---

## 3 · Uncovered analog failures (R2 buckets + landscape)

Five buckets: (1) self-report dishonesty, (2) amnesia, (3) premature completion, (4) write
collisions, (5) unbounded cost — the buckets themselves ARE covered (maker≠grader, U10/U30,
Default-FAIL/U15, U16–U19, U12–U14). But specific documented failures are NOT:

- **Residual of Bucket 1 — verifier false-pass. [UNCOVERED]** R2 says prompt-level gates "don't
  reliably prevent" false passes and R1 says the gate is "NOT a security boundary," yet no
  requirement catches a bad-but-passed change after the fact. Directly motivates the §1.3 rollback
  gap. **Fix:** requirement to detect/undo a false-pass (land-gate or post-hoc review).
- **Devin retrospectives — autonomous OVERREACH. [UNCOVERED]** Landscape row "Avoid over-promising
  autonomy" maps to no requirement. U22 covers model *refusals*, not the agent confidently doing the
  wrong thing at scale. **Fix:** a scope/authority-bounding + human-approval-before-landing
  requirement (pairs with §1.3).
- **OpenHands issue #8630 — never mined. [UNCOVERED]** R2 lists it as a "real-world footgun" but
  extracts NO claim and R3 derives NO requirement — the lesson is simply unknown. **Fix:** mine the
  issue or explicitly record it as an un-mined pointer, not silent.
- **MAS-failure survey taxonomy — R2 flagged "under-mined," R3 did NOT mine it. [UNCOVERED]** R3
  section E covers write-collisions/stuck-tasks (mechanical) but not the survey's *semantic* MAS
  failures: inter-agent misalignment, information withholding between agents, and incorrect/weak
  verification. R2 explicitly handed these to R3; R3 dropped them. **Fix:** mine the taxonomy or
  state the accepted risk (largely mitigated by single-thread-default, but say so).
- **Cognition's context-COMPRESSION recommendation — half-used. [PARTIALLY COVERED]** U14 took the
  "avoid fan-out" half; the "context-compression as the single-agent long-horizon strategy" half is
  unused. Minor — the repo already leans plain-file state — but note it.

Adequately covered (not gaps): Temporal/Airflow durability→U31/U18/U3; write collisions→U16/U17;
cost→U12/U13/U14; amnesia→U10/U30. Note only that these lean on `[REPORTED]` legs (see §2).

---

## 4 · Promised capability with NO (verified) research

- **4.1 — The orchestration layer / "OS" process model itself.** The core promised capability has
  research only about its SUB-parts (single builder/evaluator loop, memory, gates); nothing about a
  multi-goal orchestrator's own control flow, process model, or lifecycle. See §1.1. **Biggest
  anti-pattern hit.**
- **4.2 — Scheduling / event-triggered autonomy.** R1 gap #1 and R3 U28: routines.md fetched, **no
  claim verified**. A "self-improving home" implies unattended triggers (nightly re-eval, on-merge
  learn) yet cron/webhook/GitHub-event evidence is `[REPORTED]`-only. Promised; unverified.
- **4.3 — "Self-improving" automation (consolidation / "dreaming").** R1 gap #4: "no surviving claim
  substantiates an automated consolidation loop"; U5 is `[ASSUMPTION]`; self-improving-skills is
  `[REPORTED]`. Only *manual* write-back is grounded. The headline adjective is under-researched.
- **4.4 — Multi-agent coordination as a shippable base.** The only vendor-native mechanism (Agent
  Teams) is flagged EXPERIMENTAL with R1's explicit "**Do not build the OS assuming its stability.**"
  The promised multi-agent capability has only an unstable substrate.
- **4.5 — Rollback/undo (§1.3), multi-TARGET (§1.5), OS self-test (§1.4), command/UX surface (§1.2):**
  all implied by the statement/scope, all with zero research.

**PRD must:** for each, either re-research, or state "v1 does not ship this — deferred" with a
reason. 4.1 cannot be deferred (it's the product); 4.2/4.3 can be scoped to `/loop` + manual
write-back for v1 IF stated.

---

## 5 · Internal contradictions / unresolved tensions

- **5.1 — "Portable framework" vs Windows-only NTFS junctions (U24/U25).** The install mechanic is
  Windows-specific and privilege-dependent, while the product is sold as "any repo." The
  cross-platform (macOS/Linux) install mechanic is unspecified, and junctions can fail even on
  Windows without privilege. The load-bearing seam is also R1's unresolved gap #2. **Resolve:** real
  install test + a stated per-OS mechanic, or narrow the portability claim.
- **5.2 — Agent Teams "do not depend on its stability" vs requirements DERIVED from it.** U16, U17,
  U18, U20, U23 all cite agent-teams docs, yet R1 §4 says not to build on it. Requirements inherit
  an instability warning their own source issued. **Resolve:** re-ground these off Agent Teams or
  mark them "blocked on Agent Teams GA."
- **5.3 — "Solo operator / single-thread-by-default" vs the whole concurrency apparatus (E: U16–U19).**
  Four concurrency-safety requirements presuppose multiple concurrent agents/runs, but the primary
  user is solo and U14/U19 + Cognition say single-threaded by default. Is section E even v1 scope?
  **Resolve:** the PRD must decide concurrency safety is v1 or deferred-until-fan-out; don't ship the
  machinery and the "single-thread default" simultaneously without saying which governs v1.
- **5.4 — v1 scheduler `/loop` (U28) vs "survive laptop sleep" (U29).** `/loop` runs in the local
  session; a slept laptop or dead session kills it — it does NOT satisfy U29 in the same note.
  **Resolve:** either accept "v1 runs only while awake" explicitly, or U29 forces cloud/durable
  execution that scope says is out.
- **5.5 — "Objective machine-checkable done" (Default-FAIL, R1 §3) vs "prompt-level, not a security
  boundary."** The system's trust claim is undercut by its own source. The PRD cannot present
  Default-FAIL as a guarantee; it is an anti-drift guardrail that needs the §1.3 undo backstop.
- **5.6 — "Retrieval is settled — not mined" (R3 scope guard) vs U5 memory-growth erodes retrieval.**
  R3 declares retrieval closed yet U5 reopens it (unbounded append-only growth + measured context
  rot). Retrieval is not fully settled; consolidation is an open retrieval-adjacent problem.
- **5.7 — Verified-R1 / reported-R2 confidence asymmetry presented at parity.** R3 tags carry the
  weaker label but the SUBSTANCE of whole sections (E concurrency, U28 scheduling, U31 idempotency,
  U12 budget) leans on R2 `[REPORTED]`-only claims, while sitting beside fully-verified ones with no
  confidence gradient. Synthesizing them at parity would over-state confidence.

---

## Must-fix before PRD synthesis (ranked by severity)

1. **Specify the orchestrator control loop / run-lifecycle state machine (§1.1, §4.1)** — the literal
   product has no control-flow spec and no research behind it. Blocker.
2. **Resolve scheduling (§4.2/U28): re-research or lock v1 to `/loop`, and reconcile with the
   laptop-sleep contradiction (§5.4).** Biggest gap vs brief; currently zero verified support.
3. **Add rollback/undo + land-gate for bad-but-passed autonomous changes (§1.3, §3 Bucket-1
   residual, Devin overreach).** Safety-critical given the gameable gate (§5.5).
4. **Decide concurrency scope (§5.3) and re-ground U16–U19 off Agent Teams (§5.2);** downgrade the
   `[REPORTED]`-only concurrency/idempotency/budget requirements to "verify-before-build" (§2).
5. **Resolve portability-vs-Windows-junction (§5.1/U24/U25) with a real install test;** these are
   R1's unresolved gap #2 and the literal portability seam.
6. **Attach a confidence tier to every requirement and add the single-vendor + repo-doc-as-source
   caveats to the provenance header (§2).** Prevents synthesizing unverified reqs at parity.
7. **Add OS self-test/eval (§1.4) and command/UX + notification surface (§1.2/§1.6);** name
   multi-TARGET, adopter-docs, licensing as explicit in/out scope decisions (§1.5/§1.7).
8. **Mine or explicitly accept-risk the uncovered analogs: OpenHands #8630, MAS-failure taxonomy,
   Cognition context-compression (§3).**

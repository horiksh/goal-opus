# 10 · Usage-Case Examples (real, inspected)

Concrete example projects that show the pack's patterns in the wild. Unlike file 09's
synthesized methodology, these are **inspected primary artifacts** — the files were read
directly from the repo. Confidence tags per README conventions.

> **How this file was sourced.** A second research pass was attempted but **failed on API
> rate-limiting** (no report produced). The centerpiece below was instead verified by
> reading the repository and its artifact files directly (GitHub + raw file contents), so
> it is stronger than a secondary summary — but it is still a single, self-reported
> community project (see caveats).

---

## Case study — `Braffolk/fable5-world-demo`  [VERIFIED+SRC, self-reported scope]

- Source: `https://github.com/Braffolk/fable5-world-demo` (523★, 96 commits, ~21,000 lines
  of strict TypeScript).
- What it is: a procedural **4×4 km 3D open world** in the browser (three.js
  `WebGPURenderer`, TSL materials, raw WGSL compute shaders; WebGPU / Chrome 113+),
  described as *"a 3D world built by Claude Fable 5 to test its capabilities."*
- Claim: *"built roughly 99% by the model, with minimal human steering"* — the model did
  planning, architecture, implementation, debugging, and QA across extended autonomous
  sessions.
- **Caveats:** self-reported ("99%") by the author; single community project; "Fable 5"
  attribution is the author's. It is *not* an independent benchmark — but the repo, its
  commit history, and its two control artifacts are real and inspectable, which is why it
  belongs here.

### Resolving the `PROJECT_LAAS_v2` mystery
The lead file 09 marked **[UNFINDABLE]** is **actually this repo's spec file,
`PROJECT_LAAS_v2.md`** — not a standalone project. (LAAS = the world demo's internal
codename.) The prior web pass couldn't find it because it's a file *inside* this repo, not
an indexed project name. **Now verified** by direct read. This is itself the lesson: an
unverifiable name stayed a guess until a primary source resolved it.

### Why this case matters: it independently reproduces the pack's core loop
Two human inputs only, and both are exactly where the pack says a human belongs:
1. **A spec that defines *what*, not *how*** (`PROJECT_LAAS_v2.md`) — visual targets,
   numeric budgets, and *prohibited outcomes*, deliberately not prescribing implementation.
   *"Build, don't describe. No plan-approval round-trips."*
2. **Rare subjective feedback only** — *"limited to rare feedback on the things a model
   cannot judge well from static output"* (motion feel, interactive performance, artifact
   visibility while navigating). Clean articulation of the human-in-the-loop boundary (→ 04).

Everything else was closed-loop, corroborating files 03/06/07.

---

## Exemplar artifact A — `PROJECT_LAAS_v2.md` (the spec / "PRD for an autonomous build")

A real, working spec that drove a ~99%-autonomous multi-session build. Its 15 sections are
a battle-tested template for the "define done, then let it run" approach — adopt these into
`PRD-TEMPLATE.md`:

| Section | Role (maps to) |
|---|---|
| 1. **The bar** | the target + a *mandatory reference-delta loop per phase* (→ 06 verification loop) |
| 2. Six pillars | durable design principles (belongs in system prompt / invariants → 05) |
| 3. **Operating instructions** | autonomy contract: *"Build, don't describe. No plan-approval round-trips."*, modular code, no scope-reduction |
| 4. **Fixed constraints** | non-negotiables (strict TS, Vite, WebGPU, zero external assets, deterministic seeding) |
| 5. **Floors** | *quantified* performance/content budgets — numeric floors (e.g. *"≥ 5M triangles/frame in hero shots"*) |
| 6. GPU systems | the 12 required compute/render passes (capability list) |
| 7. Surface & asset law | domain rules |
| 8. Lighting/camera/post | domain rules |
| 9. Performance & instrumentation | targets + telemetry (*"60 fps @ 1440p on RTX-3060"*, HUD) |
| 10. **Verification battery** | scripted tests: reference-delta, silhouette wireframes, shadow-color sampling, bare-ground audits, repetition flights, throughput checks, contact sheets (→ 06) |
| 11. **Phase plan** | an 8-phase *gated* roadmap with phase-closing gates (→ PRD §9 milestones) |
| 12. **Banned outcomes** | *instant-fail* criteria (black shadows, cloned trees, one-file architecture…) — negative eval spec |
| 13. **Self-score rubric** | a 12-row scoring matrix anchored to reference images |
| 14. Tier-3 post-battery | optional stretch systems |
| 15. **Final acceptance — two-frame test** | a single objective acceptance gate |

**New patterns to hard-adopt (not previously in the pack):**
- **Banned/instant-fail outcomes** — a *negative* eval spec alongside the positive one.
  Cheap, unambiguous, catches regressions the positive rubric misses.
- **Self-score rubric anchored to references** — the maker scores each dimension against a
  fixed reference; pairs with the independent verifier (→ 06) rather than replacing it.
- **Phase-gated roadmap with closing gates** — each phase has an explicit gate that must
  pass before the next; the concrete shape of PRD §9 milestones.
- **A single final acceptance test** — one objective, human-legible "ship it" gate.

---

## Exemplar artifact B — `STATUS.md` (the durable memory file)

Described as *"the model's durable memory between sessions."* Its 12 sections are a
superset of file 03's STATE.md schema and **validate it in production** — plus two
additions worth adopting:

| `STATUS.md` section | Maps to STATE.md (→ 03) |
|---|---|
| 1. **Rehydration Protocol** | *read-at-start* instructions for a resuming agent — **NEW: adopt** |
| 2. Mission | project scope header |
| 3. Hard Rules Digest | invariants (system-prompt-level) |
| 4. **Verified Environment Facts** | ≈ **Verified facts** (stage 3) |
| 5. Phase Checklist (0–7) | gated milestone status |
| 6. Current Focus | ≈ **Last session** / current work |
| 7. Next Actions | prioritized queue (incl. "BINDING" constraints) |
| 8. **Key Decisions Log (D1–D6)** | an architectural decision record — **NEW: adopt** |
| 9. Architecture Map | module ownership |
| 10. Reference Image Analysis | domain targets |
| 11. Progress Snapshot | historical checkpoint |
| 12. **Gotchas / Lessons Learned** (append-only, ~40 entries) | ≈ **Lessons learned** + skill "known failure modes" (stage 4) |

**Discipline visible in the real file (quote-backed):**
- **Rigorous measurement methodology** — e.g. *"M1 Max THERMAL DRIFT: cross-run medians
  drift +50% when hot — only ABAB pairs / in-session 24-sample averages count."* (Real
  eval hygiene: control for the measurement environment.)
- **Bisected bug repros with exact coordinates + ablation flags** —
  *"BISECTED at the repro cam (-1400,131.6,1250,yaw45) … persists under ?ablate=water."*
  (Investigate-before-fixing → stage 2; reproducible, not "seems flaky.")
- **Screenshot verification recorded as a Key Decision** (the vision-QA method is itself a
  tracked architectural decision).

**New patterns to adopt into the STATE.md schema (→ 03):**
- **`## Rehydration protocol`** at the top — explicit "how to resume" for the next session
  (operationalizes read-at-start).
- **`## Key decisions log`** (ADR-style, D1, D2, …) — records *why* an architecture choice
  was made, so it isn't relitigated. This is distinct from "verified facts."

---

## Exemplar pattern C — vision self-QA loop (concrete implementation)  [VERIFIED+SRC]

The README's QA description is the in-the-wild version of file 06's vision-verify stage:
> *"The model does its own QA. It boots the world headless (Playwright driving Chromium
> with a WebGPU/Metal adapter), takes screenshots, samples pixels, diffs frames against
> baselines."*

Extractable recipe: **headless boot → screenshot → pixel sampling → frame-diff against a
stored baseline.** Note the two objective mechanisms that make it work without a human:
*pixel sampling* (check specific expected values, e.g. shadow color ≠ pure black) and
*baseline frame-diff* (regression detection). Plan the vision loop with *stored baselines*,
not just "does it look right."

---

## Additional verified example projects (research pass 2)

> Sourced by **direct read of each primary source** — the second research workflow's
> verify/synthesis phases were killed by an account session limit, so its leads were
> re-verified here by fetching the sources directly. Models are noted per project: most
> predate Fable 5 (Opus 4.5/4.6); the *patterns are model-agnostic*, consistent with this
> pack's stance. Standing caveat: these are largely Anthropic self-reported, and one
> skeptical community thread (HN #48752030) argues autonomous-coding demos may lean on
> training-data familiarity — treat scope/metrics as **claims**, patterns as reusable.

### ⭐ Reference implementation — `anthropics/cwc-long-running-agents`  [VERIFIED+SRC]
The single most useful artifact found: an **official Anthropic repo (Apache-2.0, 472★)**
that is a *working harness* implementing the exact loop this pack describes (companion to
the two harness blog posts; flagged "event demo, not maintained" — read/borrow, don't
depend). Source: `https://github.com/anthropics/cwc-long-running-agents`.
Its three quality-loop primitives map 1:1 onto the pack:
- **Default-FAIL contract** (`test-results.json`, `hooks/verify-gate.sh`) — every criterion
  starts `false`; the agent must open evidence before it may mark `passing` (a `PreToolUse`
  gate). = our locked feature-requirements/eval spine (→ 09 C4).
- **Fresh-context evaluator** (`agents/evaluator.md`) — a separate subagent with **no
  Write/Edit tools** grades from a pristine context and returns `PASS`/`NEEDS_WORK`
  (`claude --agent evaluator -p "..."`). = our independent verifier (→ 06).
- **Agent-maintained handoff** (`PROGRESS.md` + `hooks/commit-on-stop.sh`) — the agent
  writes progress notes and **commits to git on stop**; the next session resumes from
  `git log` + progress file. = write-before-walk STATE.md + git-as-memory (→ 03, 09 C3).
- Operator controls: `hooks/kill-switch.sh` (halts while an `AGENT_STOP` file exists) and
  `hooks/steer.sh` (surfaces `STEER.md` once mid-run). = human-steering points (→ 04).
- Implements the same generator/evaluator loop as Claude Code's built-in `/goal`.
- **Action:** model the M0–M1 harness on these hooks instead of inventing one.

### Multi-agent parallelism at scale — Claude's C compiler  [VERIFIED+SRC]
The definitive multi-agent case study. **Opus 4.6** wrote a **~100,000-line C compiler in
Rust** from scratch (x86-64/i686/AArch64/RISC-V64) that builds PostgreSQL, SQLite, and the
Linux kernel. Sources: `https://www.anthropic.com/engineering/building-c-compiler`,
`https://github.com/anthropics/claudes-c-compiler`.
- Scale: **~2,000 Claude Code sessions over 2 weeks, ~$20,000, 3,982 commits.** 100% of
  code by the model; a human only wrote test cases to pass (no interactive pairing).
- **Orchestration (implementable):** 16 parallel agents on a shared bare git repo, one
  Docker container each. Agents **claim tasks by writing a lock file into `current_tasks/`**;
  git sync forces two claimants to diverge; on finish each **pulls → merges → pushes →
  removes its lock**. Driver is a literal loop: `while true; do claude
  --dangerously-skip-permissions ...; done` ("when it finishes one task, it immediately
  picks up the next").
- **Memory:** frequently-updated progress files + a "running doc of **failed approaches**
  and remaining tasks"; machine-readable error logs (same "record failures too" discipline
  as → 09 C3).
- Honest caveat (from the repo): *"None of it has been validated for correctness."* Scale
  and autonomy are the claims; correctness is not.
- **Maps to:** file 04 multi-Clauding + file 05 subagent fan-out. The git-file-lock is a
  concrete complement to worktree isolation for parallel writes.

### Maker/verifier with vision — three-agent app harness  [VERIFIED+SRC]
Anthropic's Labs harness for autonomous full-stack app builds — the clearest primary-source
instance of maker/verifier + vision-verify.
Source: `https://www.anthropic.com/engineering/harness-design-long-running-apps` (Opus 4.5→4.6).
- **Planner** expands the brief into an ambitious spec; **Generator** builds in sprints, one
  feature at a time (React/Vite/FastAPI/SQLite); **Evaluator** uses the **Playwright MCP to
  click through the running app** (UI, API, DB) before scoring and writing a critique.
- **"Sprint contract negotiation":** generator + evaluator agree what "done" means **before
  any code is written** (= define-done-first → PRD §2; mirrors the Braffolk spec → exemplar A).
- Communication via files (one writes, another reads) (→ 05 comms).
- **Maps to:** file 06 verifier subagent + vision self-check — the Playwright evaluator is
  the backend/UX analogue of Braffolk's pixel-diff loop.

### Self-improving skills as an installable plugin — `UniM0cha/claude-self-improving-skills`  [VERIFIED+SRC]
A concrete implementation of "skills that compound" (→ 07) as a real MIT Claude Code plugin
(Python; ports Nous Research "Hermes Agent" procedural memory).
Source: `https://github.com/UniM0cha/claude-self-improving-skills`.
- **Loop:** complex task → a `Stop` hook detects complex work from transcript signals →
  delegates to a **background subagent** that writes/patches `~/.claude/skills/<name>/SKILL.md`
  → validates → available next session; stale skills auto-archived.
- Durable files: `~/.claude/skills/<name>/SKILL.md`, `~/.claude/self-improve/skill_usage.json`
  (use/view/patch telemetry), `team_config.json`, `~/.claude/skills/.archive/`.
- **Maps to:** file 07 — shows the *mechanism* (Stop hook + distiller subagent) to make
  write-back **structural**, plus usage telemetry to see which skills earn their keep.

### Fable-5-specific verified demos (the official announcement)  [VERIFIED+SRC / official]
From `https://www.anthropic.com/news/claude-fable-5-mythos-5`:
- **Pokémon FireRed, vision-only** — Fable 5 finished the game "using only raw game
  screenshots," where prior models "needed a complex helper harness." (Long-horizon +
  vision; the earlier Claude-plays-Pokémon used a self-managed in-prompt knowledge base the
  model could add/edit/reference — an agentic-memory precedent.) [3-0]
- **Genomics research, >1 week largely autonomous** (Mythos 5) — a second long-run duration
  point beyond the Boltzmann solver. [3-0]
- *"Fable 5 … improves its outputs using its own notes"* — self-authored-notes framing;
  marketing phrasing, attribute as a claim. [weak, 1-1]

### Community + academic lineage (lower weight)
- `pulkitxm/claude-directory` [VERIFIED, 3-0] — a real public gallery of web-UI experiments
  "generated with Claude (Fable 5)," author calls it "vibe coded." Minor, but a real
  in-the-wild Fable 5 attribution.
- Pattern lineage (landmark papers, **not** Claude-specific — cite as ancestry, not Claude
  evidence): **Voyager** (arXiv 2305.16291 — skill library of executable code +
  self-verification), **Reflexion** (2303.11366 — verbal feedback in episodic memory, no
  weight updates), **Generative Agents** (2304.03442 — a "memory stream" + reflection /
  **consolidation** = the "dreaming" idea). **ASG-SI** (2512.23760) is [UNVERIFIED] here —
  cite only after checking.

---

## Net effect on the plan

1. **A real, inspectable case study replaces the unverifiable ones** — anchor "autonomous
   multi-session build" reasoning here and on file 09's Boltzmann solver.
2. **`PROJECT_LAAS_v2` reclassified** [UNFINDABLE → VERIFIED as this repo's spec file].
3. **Adopt into `PRD-TEMPLATE.md`:** banned/instant-fail outcomes, a self-score rubric
   anchored to references, a phase-gated roadmap with closing gates, a verification
   battery, and a single final acceptance test.
4. **Adopt into the STATE.md schema (→ 03):** a `Rehydration protocol` header and a
   `Key decisions log` (ADR).
5. **Vision loop gets a concrete recipe:** headless render → screenshot → pixel-sample →
   baseline diff.
6. **A reference harness to copy, not invent:** `anthropics/cwc-long-running-agents`
   implements the whole loop as hooks (Default-FAIL contract, fresh-context evaluator,
   commit-on-stop handoff, kill-switch/steer). Base the M0–M1 harness on it.
7. **A concrete multi-agent pattern:** the C-compiler's 16-agent git-file-lock loop
   (`current_tasks/` lock files + pull/merge/push) is the implementable shape for the
   plan's parallelism (→ 04), alongside worktree isolation.
8. **A structural write-back mechanism:** the `claude-self-improving-skills` plugin shows a
   `Stop` hook + distiller subagent as the way to make skill write-back automatic (→ 07).

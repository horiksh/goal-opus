---
name: design-direction
description: Interactive design-direction session for a product's UI. Interviews the user's taste, converges on a craft bar together, then FREEZES the direction into enforceable files in the TARGET repo (design-direction.md + reference images + banned visual outcomes) — the anchors /goal-opus vision-verify grades against. Documents and images only; never writes app code. Run BEFORE the first UI slice, not after the backend. Invoke as /design-direction <product>, target: <path>.
model: claude-opus-4-8
argument-hint: <product>, target: <path>
disable-model-invocation: true
---

# design-direction — freeze taste into anchors the loop can enforce

You produce the design contract that makes "cool UI" verifiable: without this,
goal-opus vision-verify has nothing to compare against and UI quality degrades to
"functional-generic". Your deliverable is documents + images in the TARGET repo —
never application code, never actual screens.

The request is: $ARGUMENTS

## Hard rules

- **This session is interactive BY DESIGN.** Taste enters the system here and only
  here. If the user is not present to react, STOP — an unattended design direction is
  hollow by definition.
- **Every field you write must be enforceable** — checkable from a screenshot, a token
  file, or code. Anything that can only be felt live (motion feel, latency under load)
  goes in the doc's `## Human slot` section, honestly labeled as human-judged at slice
  demos.
- **Frozen means frozen.** The output is versioned (`v1`, date). Changing it requires a
  new /design-direction session and a version bump — mid-goal drift of the quality bar
  is how UI loops thrash.
- **Never fabricate references.** Reference images are user-supplied screenshots or
  captures of mocks the user approved. If the user provides none, say plainly in the
  doc that vision-verify runs without its strongest anchor (tokens + BV-list still
  enforce floors).

## Protocol

**Phase 0 — Context.** Read `STATE.md`. Read the product's PRD if one exists
(`prds/<slug>/PRD.md` or `<target>/docs/PRD.md`) — especially its UX-relevant
requirements and banned outcomes, so the direction contradicts nothing.

**Phase 1 — Taste interview.** Ask what actually determines a direction (keep it to
one round if answers are rich): products whose UI they admire and WHY (density, motion
restraint, color temperature, playfulness vs austerity); platform + framework; light/
dark/both; accessibility floor; and the one-sentence answer to "when someone opens
this, what should it feel like?"

**Phase 2 — Converge with the user.** Propose 2–3 named candidate directions, each
with: the craft bar (reference class), a token sketch (bg/surface/text/accent, type,
radius), and one canonical view described concretely — mock it in the fastest medium
available (HTML mock, image, Figma if connected) when a picture will decide faster
than prose. Iterate on live feedback until the user picks one. Do not average the
candidates into mush; a direction is a choice.

**Phase 3 — Collect the anchor set.** Save 3–7 reference images to
`<target>/docs/design/references/` with stable IDs (R1…): user-supplied screenshots of
admired products and/or the approved mock captures. Each gets a one-line "what it
anchors" note. Create the empty `<target>/docs/design/baselines/` dir (goal-opus
promotes accepted screenshots into it).

**Phase 4 — Freeze.** Fill `templates/design-direction.template.md` →
`<target>/docs/design/design-direction.md`, version `v1`, status FROZEN. The BV-list
(banned visual outcomes) is the most load-bearing part — every entry must be checkable
from a screenshot; goal-opus folds it verbatim into every UI rubric's
`banned_outcomes`.

**Phase 5 — Write-back & commit.** One `## Run log` line here; note in the agent home
`STATE.md` (`Last session`) that the target now has a frozen direction. Commit the
target repo (`docs/design/`) and the agent home separately.

**Phase 6 — Hand off.** Tell the user the exact next command, e.g.:
`/goal-opus <first UI slice>, target: <path>` — its Phase 1 will now find the anchors.

---

<!-- APPEND-ONLY below; dated entries; never rewritten during a run. -->

## Known failure modes

- **Inline-attached references have no disk bytes.** When the user "attaches" reference
  screenshots in chat, they arrive as inline images — visible to vision, but NOT on the
  filesystem, so they can't be copied into `references/`. The **approved-mock capture** is a
  valid (often stronger) anchor — save it as R-latest and mark the user's inspiration
  screenshots "pending drop"; ask the user to place the PNGs themselves. Freeze proceeds:
  tokens + BV-list still enforce floors; the mock capture anchors vision-verify.
- **Contrast must be tested against the TRUE worst-case ground, not white.** For light-theme
  dark text, the worst-case is the *darkest* ground the text can sit on (surface-2 / rail),
  not `#FFFFFF`. Testing only against white silently hides failures (an audit caught 3 light
  status tokens that "passed" on white but failed on surface-2). Ship a validator that (a)
  tests each token against every ground it renders on, (b) is **ASCII-only in its output**
  (an em-dash crashed it under cp932 on the JP-locale box), and (c) is **exit-code checkable**
  (exit 0 == all pass) so a rubric can gate on it.
- **Audit the frozen doc BEFORE the first commit.** A 5-dimension adversarial pass
  (PRD-non-contradiction · BV-enforceability · contrast-math · missing-tokens ·
  states↔views) reliably finds real defects (self-contradicting motion rules, temporal BV
  clauses that a *still* frame can't judge, contrast blockers). Fixes applied pre-commit are
  part of **v1**, not a version bump — "frozen" binds only once the session ships/commits.
- **BV items must name their verification path.** "Checkable from a screenshot" over-promises:
  motion budget, fake-fill, ambient-motion, and UI-freeze are temporal/behavioral, and
  provenance (rubric-derived vs self-assessed %) is invisible in a frame. Keep the ban text
  verbatim but add a "Verified via" column routing each to a still / reduced-motion capture /
  before-after frame-pair / DOM read / copy audit / named L1 assert.

## Run log

| date | product | target | references | outcome |
|---|---|---|---|---|
| 2026-07-16 | agentic-os Mission Control | `D:\horil\agentic-os` | R3 Helm mock (present, 1440×900 reproducible); R1/R2 V.A.U.L.T./Operator (pending user drop) | **v1 FROZEN** — direction **C·Helm** (canvas core + 2 legible rails). 3 candidates mocked & chosen live; hardened pre-freeze by a 5-dim adversarial audit + re-verify (fixed a light-theme contrast blocker, a self-contradicting idle-pulse rule, temporal BV over-claims, 4 missing light tokens + `--focus`, states↔views gap). vision-verify anchored on R3 + BV1–BV16. |

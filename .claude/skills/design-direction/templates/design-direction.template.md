# Design direction — <product> · v1

> Status: **FROZEN <yyyy-mm-dd>** by /design-direction. Changes require a new session
> and a version bump — the quality bar does not drift mid-goal.
> Consumed by: /goal-opus vision-verify (anchors + BV-list) and every UI-slice rubric.

## The feel (one sentence)
<"When someone opens this, it should feel …" — the user's own words.>

## Craft bar (reference class)
<Which products set the bar, and specifically WHAT to match: density, motion restraint,
type discipline, use of color. E.g. "Linear's information density and keyboard-first
speed; Raycast's restraint — accent color is earned, not ambient.">

## Reference images (the anchor set — vision-verify compares against THESE)
| ID | File | What it anchors |
|---|---|---|
| R1 | references/R1-<name>.png | <e.g. overall density + hierarchy of the main view> |
| R2 | references/R2-<name>.png | <e.g. how empty states are treated> |

## Design tokens (the contract; code copies THESE, not vice versa)
- **Color** (light / dark): bg · surface · border · text-primary · text-muted ·
  accent · success · warning · danger — exact values.
- **Type:** family; scale (sizes/weights/line-heights); mono usage.
- **Space & shape:** spacing scale; radius scale; elevation/shadow rules.
- Token file in code: `<target>/<path>` — a rubric may diff code tokens against this
  table.

## Interaction principles
- <keyboard-first? click-first? latency budget for interactions (e.g. <100ms feedback)?>
- <density: comfortable / compact; information-per-screen stance>
- **Motion rules:** durations + easing; what animates; what NEVER animates.

## Required states (every surface ships all four, designed — not library defaults)
**empty · loading · error · stale.** <Per-state treatment: tone of empty-state copy,
skeleton vs spinner, error affordance.>

## Banned visual outcomes (BV-list — folded verbatim into every UI rubric's banned_outcomes)
| ID | Outcome (must be checkable from a screenshot) |
|---|---|
| BV1 | Unthemed component-library defaults visible (stock shadcn/Bootstrap look) |
| BV2 | Any surface missing a designed empty/loading/error/stale state |
| BV3 | Layout breaks or horizontal scroll at <widths, e.g. 1280 / 1024 px> |
| BV4 | Text contrast below <e.g. WCAG AA 4.5:1> on any reference-view capture |
| BV5 | <product-specific — add per direction> |

## Screenshot procedure (scripted, reproducible — rubrics reference these commands)
- Boot: `<exact command to launch the surface deterministically>`
- Capture, per canonical view, at fixed viewport + theme:
  `<e.g. npx playwright screenshot --viewport-size=1440,900 <url> <out>.png>`
- Canonical views: `<view-1>`, `<view-2>`, … (names are stable; baselines key on them)
- Baselines dir: `docs/design/baselines/` (written ONLY by the goal-opus orchestrator
  on accepted passes).

## Human slot (honestly not screenshot-checkable — judged by the user at slice demos)
- Motion feel; interactive performance under a real run; <anything else felt, not seen>.

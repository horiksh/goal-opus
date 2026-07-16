# R5 — Skills-Inventory, Onboarding/Learnability, Visionary-but-Legible

Research closing three gaps an adversarial gap-check found missing. Scope: narrow + deep on
(1) installed-capabilities inventory UI, (2) first-run onboarding/learnability for complex operator
tools, (3) concrete "visionary yet legible" live-agent visualization. General dashboard best-practice
is out of scope (covered by R1). Every claim carries an epistemic tag + a one-line PRD implication.

Tags: `[VERIFIED+SRC]` = primary source read in full · `[REPORTED]` = secondary / read via search
summary of an official or credible source · `[ASSUMPTION]` = inference, with verification path.

Product recap: local-first, file-based, single-operator, Windows-first CLI framework running a
bounded self-improving loop (maker → independent verifier → land-gate → write-back), surfaced as a
localhost dashboard. A "skill" here = a Claude-Code payload (SKILL.md + installed agents + tools)
under a repo's `.claude/`. The operator's own words: make it "intuitive and visionary" and let them
SEE "skills installed, tokens, running projects, % to goal."

---

## GAP 1 — SKILLS-INSTALLED VISUALIZATION (installed-capabilities inventory)

The user's FIRST-named mechanic. The dominant, directly-applicable analog is **Claude Code's own
plugin/skill model** — the very substrate this product wraps — so its data model is authoritative
for what a "skill card" can and should show. VS Code / Obsidian / Raycast / dependency dashboards
supply the failure modes and the enrichment fields.

### 1.1 Claude Code's own inventory model (authoritative analog)

- **`claude plugin list` already enumerates installed plugins "with their version, source marketplace,
  and enable status," filterable by `--enabled`/`--disabled`.**
  `[VERIFIED+SRC https://code.claude.com/docs/en/plugins-reference]`
  PRD implication: the inventory's baseline columns are non-negotiable — name, version, source, enabled?
  — because the underlying CLI already exposes exactly these; the dashboard should render them, not invent a different schema.

- **`claude plugin details <name>` shows a per-plugin "component inventory" grouped as Skills / Agents /
  Hooks / MCP servers / LSP servers, PLUS a projected token cost split into "Always-on" (added to every
  session) and "On-invoke" (paid each time a component fires), per component.**
  `[VERIFIED+SRC https://code.claude.com/docs/en/plugins-reference]`
  PRD implication: a skill card MUST show its component breakdown AND a two-number token cost (always-on vs
  on-invoke) — this is the concrete bridge between the "skills installed" and "tokens" mechanics the user named, and it already exists as data.

- **A plugin's identity metadata schema includes `name`, `displayName`, `version`, `description`,
  `author` (name/email/url), `homepage`, `repository`, `license`, `keywords`, and `defaultEnabled`;
  install scope is one of `user` / `project` / `local` / `managed`.**
  `[VERIFIED+SRC https://code.claude.com/docs/en/plugins-reference]`
  PRD implication: card fields (author/provenance, repo link, license, scope badge) come straight from the
  manifest — provenance is free data, so "unknown provenance" would be a UI omission, not a data gap.

- **Trust/permission is first-class and asymmetric: project-scope skills/plugins load only after a
  workspace trust dialog; bundled MCP servers go through per-server approval; LSP/monitors are gated;
  and agents can ship `disallowedTools` — but `hooks`, `mcpServers`, `permissionMode` are forbidden on
  plugin-shipped agents "for security reasons."**
  `[VERIFIED+SRC https://code.claude.com/docs/en/plugins-reference]`
  PRD implication: each capability card MUST carry a trust/permission facet — scope (trusted workspace vs
  personal), whether it can run code (hooks/MCP/monitors), and what tools it's allowed/denied — so the operator can answer "what can this thing do to my repo?" at a glance.

- **`defaultEnabled: false` lets a plugin install in a DISABLED state; enable-state is resolved by
  precedence (explicit user setting > dependency requirement > default), and disabling a plugin
  mid-session does NOT stop already-running monitors.**
  `[VERIFIED+SRC https://code.claude.com/docs/en/plugins-reference]`
  PRD implication: "installed" ≠ "enabled" ≠ "currently active." The UI needs three distinct states, and a
  live "still running despite disable" indicator, or the operator will misread what is actually affecting the loop right now.

- **`/plugin` has a dedicated Errors tab, surfaces "which server is active" warnings when two LSP servers
  claim the same extension, warns about ignored folders, and shows the persistent-data-directory size
  before deletion.**
  `[VERIFIED+SRC https://code.claude.com/docs/en/plugins-reference]`
  PRD implication: the inventory needs an error/health surface per skill (mis-manifested, binary missing,
  conflicting) — a "broken/degraded" state is as important as "enabled," and disk/data footprint is a real per-skill attribute worth showing.

### 1.2 Cross-tool failure modes and enrichment fields

- **VS Code exposes `@installed` and `@enabled` filters, per-extension enable/disable that can be scoped
  "globally or only in the current workspace," and a non-destructive Disable (re-enable later) — the
  existence of a dedicated `@enabled` filter is itself evidence that "which of my installed extensions
  are actually active" is a recurring user question.**
  `[REPORTED https://code.visualstudio.com/docs/configure/extensions/extensions]`
  PRD implication: ship an "active only" filter/default view; global-vs-project scope must be a visible toggle on each card, not buried.

- **VS Code marketplace hosts 28,000+ extensions and "it is not uncommon that users have 50 or more
  installed," which is why Profiles exist to load only what a given workload needs — extension bloat and
  "reload required" churn are documented, named pain points.**
  `[REPORTED https://code.visualstudio.com/docs/configure/extensions/extensions]`
  PRD implication: design for bloat from day one — grouping, "unused/last-used" signals, and a per-project
  (not just global) lens; assume the operator will accumulate skills and lose track of which matter.

- **Obsidian community plugins run third-party code that "inherits Obsidian's access level" (read files,
  network, install programs); Obsidian "cannot reliably restrict plugins to specific permissions," so
  the only real control is a global Restricted Mode + per-plugin enable toggle.**
  `[REPORTED https://obsidian.md/help/plugin-security]`
  PRD implication: trust opacity is the recurring complaint when permissions can't be scoped — so the card
  MUST make the blunt facts legible (this skill can run code / touch the network / write files), since granular permission control may not exist.

- **Raycast surfaces installed extensions as sidebar entries with per-command enable/disable toggles and
  per-extension preferences/auth, and — critically — distinguishes provenance: auto-update applies only
  to Store-installed extensions, while locally-imported dev extensions are "managed by you and aren't
  updated."**
  `[REPORTED https://manual.raycast.com/extensions]`
  PRD implication: provenance (store/marketplace vs local-dev vs skills-dir) drives update behavior and
  trust — the card MUST label the source and whether updates are automatic vs manual/self-managed.

- **`npm outdated` renders exactly three version columns — Current (installed), Wanted (max in semver
  range), Latest (registry) — the canonical "is this current?" triad.**
  `[REPORTED https://docs.npmjs.com/cli/v11/commands/npm-outdated/]`
  PRD implication: "update available" is not a boolean; show installed vs latest (and whether an update is
  in-range vs a major jump) so the operator can judge risk, not just see a badge.

- **Renovate's key UX win over Dependabot is a single aggregate "Dependency Dashboard" — "a running list
  of pending, pinned, and rate-limited updates in one place" — whereas Dependabot's per-repo PRs have
  "no aggregate view," a named complaint.**
  `[REPORTED https://reintech.io/blog/dependabot-vs-renovate-snyk-dependency-management-tools-compared]`
  PRD implication: provide ONE consolidated "what's installed across all my projects + what's stale" view,
  not a per-repo hunt — aggregate legibility is the differentiator operators praise.

- **Claude Code's real-world skill/MCP complaint is context/token opacity: tool + skill definitions load
  at session start and "present in every message," and community reports cite MCP setups burning
  55,000–66,000+ tokens before a single message — "difficult to understand which specific skills are
  active."**
  `[REPORTED https://scottspence.com/posts/optimising-mcp-server-context-usage-in-claude-code]`
  PRD implication: tie each installed skill to its standing context cost and a "did it fire this run?"
  signal — the operator's actual pain is invisible always-on cost + not knowing which skill did anything.

### GAP 1 — What the "installed-skill card" MUST show (concrete)
1. **Name** (`displayName` if present, else `name`) + one-line description.
2. **Version** + update state: installed vs latest, and in-range vs major-jump (npm triad, not a boolean).
3. **Source / provenance**: marketplace vs local `@skills-dir` vs project-checked-in; auto-update vs self-managed.
4. **Scope badge**: user / project / local / managed (personal vs trusted-workspace).
5. **Three-state status**: installed · enabled · currently-active-this-run (+ "still running despite disable" edge).
6. **Component inventory**: counts of skills / agents / tools(MCP) / hooks / LSP it contributes.
7. **Token cost**: always-on (every session) + on-invoke (per fire) — the skills↔tokens bridge.
8. **Trust / capability facet**: can it run code, touch network, write files; allowed/denied tools.
9. **Health/errors**: mis-manifest, missing binary, conflict, degraded — a visible "broken" state.
10. **Last-used / did-it-fire**: recency + whether it participated in the current/last loop iteration.
11. **Provenance links**: author, repository, homepage, license.
12. **Footprint**: persistent-data-dir / disk size (optional, per-skill).

---

## GAP 2 — ONBOARDING & LEARNABILITY (the "intuitive" claim)

The hard part is not a product tour; it is making a NOVEL mechanic (maker → verifier → land-gate →
write-back, Default-FAIL rubric, criteria %) legible to an operator who didn't build it. Evidence
converges on: empty-state-as-teacher, in-context "pull" help over forced tutorials, progressive
disclosure, and radically reduced first-run setup.

- **NN/g's three empty-state guidelines for complex apps: (1) communicate system status ("There are no
  records to display…"), (2) provide contextual learning cues ("pull revelations" shown once the user
  starts a task), (3) provide direct pathways to the key task (explicit instructions or a link to the
  exact next step).**
  `[VERIFIED+SRC https://www.nngroup.com/articles/empty-state-interface-design/]`
  PRD implication: every empty region (no projects, no skills, no runs yet) is an onboarding surface and
  MUST do all three — state why it's empty, teach the mechanic in context, and offer the one next action (e.g., "Start your first goal loop").

- **NN/g: in-context help "can be applied right away and is thus more memorable" — contextual cues beat
  forced upfront tutorials for teaching how an application works.**
  `[VERIFIED+SRC https://www.nngroup.com/articles/empty-state-interface-design/]`
  PRD implication: prefer inline "what am I looking at?" affordances anchored to each mechanic over a modal
  product tour; teach the loop where the loop is shown, at the moment it matters.

- **Progressive disclosure is the primary defense against onboarding overwhelm: "most user onboarding
  failures trace back to too many features surfaced too early," and complex, data-dense dashboards should
  "present critical information first, with expandable sections for deeper detail."**
  `[REPORTED https://userpilot.com/blog/progressive-disclosure-examples/]`
  PRD implication: default view shows only the loop's headline state (% to goal, current phase, token burn);
  push rubric internals, per-criterion detail, and evidence behind expand/drill-down — legible by default, deep on demand.

- **First-run setup should be radically reduced: replace an empty editor with "a filled example document
  the user can modify," and cut setup "from multiple required fields to one essential field, with
  everything else having smart defaults."**
  `[REPORTED https://www.nngroup.com/articles/onboarding-tutorials/]`
  PRD implication: ship a seeded example goal/loop the operator can watch run once (a "demo loop"), and make
  the real first-run ask for one thing (a goal), defaulting the rest — seeing the mechanic run beats reading about it.

- **Novel mechanics genuinely take weeks to internalize: Temporal (a comparable durable-execution loop
  system) has "a steep learning curve," with "most developers 2–4 weeks before they're comfortable,"
  requiring "a mental shift to understand determinism."**
  `[REPORTED https://medium.com/@thinhda/temporal-vs-airflow-a-comparative-analysis-915d2954f592]`
  PRD implication: budget for a real learning curve — persistent (not one-time) glossary/legend affordances
  for the invented vocabulary (maker, verifier, land-gate, Default-FAIL, criteria) so the operator can re-learn a term the 5th time they see it, not just the 1st.

- **Temporal's operator UI is a cautionary tale: it "provides an interface with execution history, [but]
  with complex workflows there may be thousands of events, making it difficult to debug" — raw
  event-history dumps overwhelm rather than explain.**
  `[REPORTED https://thinhdanggroup.github.io/temporal-airflow/]`
  PRD implication: do NOT render the loop as an undifferentiated event log; abstract each iteration into a
  legible unit (maker→verifier→gate→write-back as four labeled stages with pass/fail) and let the operator drill into events only on demand.

- **LangGraph Studio ("the first agent IDE") makes a running agent legible by rendering the agent as a
  node/edge graph and streaming "real-time information about what steps are happening — you can see the
  agent decide which tools to call, call those tools, and then continue looping," plus pause/interrupt
  and step-through.**
  `[VERIFIED+SRC https://www.langchain.com/blog/langgraph-studio-the-first-agent-ide]`
  PRD implication: the most intuitive representation of a loop is the loop itself drawn as a small graph
  with a live "you are here" marker on the current stage — this doubles as onboarding (the diagram teaches the mechanic) and as live status.

### GAP 2 — What the onboarding/learnability layer MUST show (concrete)
1. **Empty states that teach**: for each zero-content region (no goals / no skills / no runs), state the
   status, explain the mechanic in one sentence, and offer the single next action.
2. **A watchable demo loop**: a pre-seeded example goal the operator can run once to see maker→verifier→
   gate→write-back happen, before committing their own goal.
3. **One-field first-run**: ask only for the goal; smart-default rubric/scope/model, editable later.
4. **Persistent legend/glossary** for invented terms (maker, verifier, land-gate, Default-FAIL, criteria %),
   reachable in-context, not a one-time tour.
5. **Inline "explain this" affordance** on every novel widget (the % ring, the phase indicator, the rubric),
   answering "what am I looking at?" where it stands.
6. **Progressive disclosure**: headline loop state by default; rubric internals, per-criterion pass/fail,
   token detail, and evidence behind expand/drill-down.
7. **The loop drawn as a labeled 4-stage diagram** with a live current-stage marker — the diagram is both the
   mental model and the status display.

---

## GAP 3 — VISIONARY / CUTTING-EDGE, YET LEGIBLE

Resolving the tension: "visionary" ≠ gratuitous motion/dark-mode. The credible resolution is a novel,
information-rich, LIVE visualization of the agent LOOP itself, rendered beautifully but governed by
functional-motion and glanceability rules so it stays legible.

- **NN/g's functional-motion doctrine gives the honest boundary: motion is legitimate for (1) feedback
  that an action registered, (2) communicating a state/mode change, (3) spatial navigation, (4)
  signifiers — but "motion in user interfaces can easily become annoying: it's hard to stop attending to
  it, and, if irrelevant to the task at hand, it can substantially degrade the user experience," and
  should be "subtle, unobtrusive, and brief."**
  `[VERIFIED+SRC https://www.nngroup.com/articles/animation-purpose-ux/]`
  PRD implication: every animation in the "alive" visualization must map to a real state change in the loop
  (phase transition, criterion flipping pass/fail, token tick, gate decision); ban ambient motion that doesn't encode state. This is the concrete definition of "visionary but legible."

- **NN/g: peripheral vision inherently detects motion, so "multiple simultaneous animations create
  competing attention demands, diminishing effectiveness."**
  `[VERIFIED+SRC https://www.nngroup.com/articles/animation-purpose-ux/]`
  PRD implication: at most one focal live animation at a time (the currently-active loop stage); everything
  else holds still or updates discretely — motion budget is a design constraint, reconciling "alive" with "5–9 calm elements."

- **The "coming alive" pattern already exists and is credible: LangGraph Studio streams a running agent as
  a live-updating node graph where "the entire workflow is displayed as a live visualization… updated in
  real-time," letting you watch it "decide which tool to call… and then continue looping."**
  `[VERIFIED+SRC https://www.langchain.com/blog/langgraph-studio-the-first-agent-ide]`
  PRD implication: the flagship "visionary" element is a live loop-graph (maker→verifier→gate→write-back)
  that animates the active stage and pulses on transitions — this is information-rich AND premium, not decorative.

- **Agent-run "flight recorder" timelines are the emerging premium pattern: Honeycomb's Agent Timeline
  "renders an entire multi-agent conversation as a visual sequence, showing every agent, trace, tool
  call, and failure chronologically," and good run views let you "play/pause… and observe how the agent
  is working in real-time."**
  `[REPORTED https://www.honeycomb.io/platform/agent-timeline]`
  PRD implication: pair the live loop-graph with a scrubable per-iteration timeline (play/pause the run,
  step through stages) — legible depth on demand, and it reads as cutting-edge because it's genuinely novel information, not eye-candy.

- **Glanceability is the discipline that keeps "alive" legible: a glanceable interface "communicates its
  key message in one to two seconds," exploiting preattentive processing (color, motion, shape, position
  decoded in <250 ms) — motion is a preattentive channel, so it can encode state at a glance if used
  sparingly.**
  `[REPORTED https://uxdesign.cc/glanceable-ux-turning-information-into-instant-understanding-bc2317283ef4]`
  PRD implication: use motion/color/position as preattentive encodings of loop state (green pulse = criterion
  passed, the % ring filling, a token counter ticking) so the operator reads "how's it going?" in ~1 second without parsing text.

- **Stephen Few's operational-dashboard doctrine sets the taste ceiling: the best operational dashboards
  are "real-time, glanceable, and calibrated to surface the exceptions that actually need attention" —
  premium = surfacing the one thing that needs the operator, not maximal visual density.**
  `[REPORTED https://www.intelligentgraphicandcode.com/design/dashboard-design/operational-dashboards]`
  PRD implication: "visionary" should express itself as exception-surfacing (the loop stalled / verifier
  FAILed / gate blocked / token budget nearing) rising to the foreground, calm otherwise — restraint IS the premium feel, not a compromise against it.

- **The 2024–2026 "premium dev tool" reference set (Linear, Vercel, Warp, Raycast) earns its cutting-edge
  reputation through precision + speed + restraint — Linear is "designed to the last pixel… built for
  speed with 50ms interactions and real-time sync," not through heavy ornamentation.**
  `[REPORTED https://linear.app]`
  PRD implication: chase the Linear-class feel via responsiveness (instant local-first updates, real-time
  loop sync, sub-100ms interactions) and pixel precision, NOT via more animation — perceived performance is the dominant driver of "premium," and it's fully compatible with calm restraint.

- **Functional animation has a measurable comprehension payoff, not just aesthetics: reporting on
  purposeful UI motion cites users processing information faster when "animations have a clear purpose,"
  reinforcing that state-encoding motion aids rather than harms.**
  `[REPORTED https://www.mockplus.com/blog/post/20-motion-design-principles-with-examples]`
  PRD implication: justify each live animation by the comprehension it buys (faster read of loop state);
  if an animation doesn't make the loop's state faster to read, it fails the bar and is cut.

### GAP 3 — The honest resolution (for the PRD narrative)
"Visionary" = a **live, information-rich visualization of the agent loop itself** — the maker→verifier→
land-gate→write-back cycle drawn as a graph/timeline, with criteria flipping pass/fail and tokens
burning, animated ONLY where motion encodes a real state change, governed by a one-focal-animation-
at-a-time budget and glanceable (<2s read) preattentive encodings, with exceptions surfacing to the
foreground and calm restraint otherwise. It is cutting-edge because the *thing being shown* is novel and
premium because it is fast, precise, and legible — NOT because it is animated or dark. This directly
reconciles the user's "visionary" ambition with best-practice "calm restraint."

---

## Source ledger (deduped)
- Claude Code Plugins reference (primary, read in full): https://code.claude.com/docs/en/plugins-reference
- NN/g — Empty states in complex apps (primary): https://www.nngroup.com/articles/empty-state-interface-design/
- NN/g — Animation & motion in UX (primary): https://www.nngroup.com/articles/animation-purpose-ux/
- NN/g — Onboarding tutorials vs contextual help (primary): https://www.nngroup.com/articles/onboarding-tutorials/
- LangGraph Studio: the first agent IDE (primary vendor): https://www.langchain.com/blog/langgraph-studio-the-first-agent-ide
- VS Code — Use extensions (official docs): https://code.visualstudio.com/docs/configure/extensions/extensions
- VS Code — Workspace Trust (official docs): https://code.visualstudio.com/docs/editing/workspaces/workspace-trust
- Obsidian — Plugin security (official help): https://obsidian.md/help/plugin-security
- Raycast — Extensions manual (official): https://manual.raycast.com/extensions
- npm — npm-outdated (official docs): https://docs.npmjs.com/cli/v11/commands/npm-outdated/
- Renovate vs Dependabot vs Snyk (secondary): https://reintech.io/blog/dependabot-vs-renovate-snyk-dependency-management-tools-compared
- Temporal vs Airflow (secondary): https://medium.com/@thinhda/temporal-vs-airflow-a-comparative-analysis-915d2954f592 ; https://thinhdanggroup.github.io/temporal-airflow/
- Claude Code MCP/skill context cost (secondary): https://scottspence.com/posts/optimising-mcp-server-context-usage-in-claude-code
- Progressive disclosure examples (secondary): https://userpilot.com/blog/progressive-disclosure-examples/
- Honeycomb Agent Timeline (vendor): https://www.honeycomb.io/platform/agent-timeline
- Glanceable UX (secondary): https://uxdesign.cc/glanceable-ux-turning-information-into-instant-understanding-bc2317283ef4
- Operational dashboards / Stephen Few doctrine (secondary): https://www.intelligentgraphicandcode.com/design/dashboard-design/operational-dashboards
- Linear (vendor, premium-feel reference): https://linear.app
- Functional motion principles (secondary): https://www.mockplus.com/blog/post/20-motion-design-principles-with-examples

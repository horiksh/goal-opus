# 04 · Orchestration — Verification Loops, /loop, Routines, Multi-Clauding

Source: "Stop Babysitting Your Agents" (Sid) and "Proactive Agents / Routines" (Maya).

## Table stakes (do these before any loop)  [VERIFIED — talk]

- **A high-quality `CLAUDE.md`** — described as the single highest-leverage thing you
  can do. It is the persistent context the agent reads on every run.
- **Connect your tools** — if a tool (Slack, Linear, Datadog, BigQuery, GitHub…) is
  useful to you, it's useful to Claude for stitching richer context.
- **Decouple compute from the laptop** — Claude Code on the web / managed containers,
  so a closed laptop doesn't kill the run.

## Pattern 1 — Verification loops (the engine)  [VERIFIED — talk]

A loop is an autonomous circuit where the agent **hill-climbs on a task using tools to
verify its own work**, instead of a human hand-holding each step:

```
write code → build & run app → exercise it (click the button / hit the route)
   → observe failure → read logs → fix → hot reload → (repeat) → open PR
```

Flavors, by surface:
- **UX:** drive a real browser, take screenshots, iterate against the visual goal.
- **Backend:** run the service, hit the route, check the DB, read logs.
- **E2E:** deploy to staging, replay production traffic.

**Distribute the loop as a self-improving Skill.** Once a verification loop works,
package it as a skill and add the rule: *"Every time you hit a blocker, edit your own
skill file to document the solution for next time."* The team contributes to it; it
sharpens on every run. (Demoed live on the Monkeytype app: spin up a dev server, use a
browser MCP to test the front end, check logs, fix lint, confirm it works — then save
the learnings into `skill.md`.)

> Takeaway: be the agent's training wheels a few times, then let it drive. Show it how
> to verify, have it summarize learnings into a skill, package for the team.

## Pattern 2 — Multi-Clauding (parallelism)  [VERIFIED — talk]

Once verification is reliable, run multiple instances at once. The bottleneck becomes
*your attention*, so use a control plane:
- **Desktop app** — GUI to manage many sessions across terminal, cloud, and repos.
- **`claude agents` view** — terminal equivalent; sorts sessions by how much attention
  each needs.
- **Cloud execution** — sessions run remotely; local compute is irrelevant.
- **Remote control** (`/remote-control`) — watch/steer any session from your phone;
  it buzzes you only when it needs input.

Combine verification + multi-Clauding → you stop babysitting and start *managing* a team
of autonomous agents.

**Concrete at-scale example (→ 10):** Anthropic's C-compiler build ran **16 parallel
agents** on a shared bare git repo, coordinating via lock files in a `current_tasks/`
directory (claim → pull → merge → push → release) inside a `while true; do claude …; done`
loop — an implementable multi-agent pattern alongside worktree isolation.

## Pattern 3 — `/loop` (run on an interval)  [VERIFIED — talk]

`/loop <interval> <prompt>` wakes the session on a cadence and re-runs the prompt.
Example: `/loop 10m babysit my open PRs` — every 10 minutes it works review comments,
merge conflicts, CI failures. Good for bookkeeping work that needs *a loop*, not *you*:
babysitting PRs, keeping CI green, updating docs, triaging feedback.

## Routines (`/schedule`) — `/loop` but remote  [VERIFIED — talk]

**Routines** are saved Claude Code configurations that run on **managed cloud
infrastructure** (the same containers as Claude Code on the web) on a trigger. Laptop
can be off. Set them up with `/schedule` (or the Web/Desktop routines tab). Anthropic
handles hosting, session state, and connector auth. Each routine is a real Claude Code
session you can **open, watch, steer, and resume** from Web/CLI/Desktop.

**Three decisions when creating a routine:**
1. **Trigger — when does it run?** Time-based (schedule) or event-based (native GitHub
   events, custom webhooks — e.g., issue opened, release published, label added).
2. **Context — what must it know?** Repositories, connectors, briefs/docs.
3. **Steering — how do you keep it honest?** Agent-on-agent review, human-in-the-loop
   (in the loop but not at the keyboard), or verification loops.

Real examples from the talks: a routine that reviews changes merged to `main` weekly
and opens a docs-update PR; a routine that posts incoming issues/feedback to Slack every
6 hours; a routine that investigates a newly-opened GitHub issue, checks for doc gaps,
and opens a PR.

## Self-improvement trigger patterns (map triggers → compounding)

- **Schedule (e.g., daily 7am)** — the "morning briefing"/consolidation pattern:
  re-run the eval suite against latest skills; distill newly-passing cases into skills;
  log newly-failing ones into STATE.md; post a digest. The system sharpens overnight.
- **API / webhook (fire on event)** — CI fails → investigate; alert fires → triage.
- **GitHub events (learn from real work)** — on PR open, eval against current skills;
  on merge, write any new pattern the PR introduced back into the skill.

## Dynamic Workflows (deterministic multi-agent orchestration)  [VERIFIED — feature]

For complex multi-step orchestration, a workflow is a JS harness the model writes on the
fly with `agent()`, `parallel()`, and `pipeline()` primitives, custom-built per task so
every stage runs in the right order. Patterns worth planning around:
- **Fan-out-and-synthesize** — split into N independent pieces, one agent each (clean
  context per piece), merge. E.g., grade N skill rules against N historical cases.
- **Adversarial verification** — per maker, spawn an independent verifier with no view
  of the maker's reasoning (the structural fix in `06-...`).
- **Loop-until-done** — keep spawning agents until a stop condition (no new findings,
  logs clean, criterion met). Pair with an objective completion check.

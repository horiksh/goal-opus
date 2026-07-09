# 05 · Tool, Skill, or Subagent? — Agent Decomposition

Source: "Tool, Skill, or Subagent?" (Will). This is the core architecture-quality talk.

## The failure the system must design out  [VERIFIED — talk]

The common decay path: an agent ships, works, then capability gets *bolted on* over
weeks. The system prompt grows to ~400 lines, the tool count balloons to ~12 (some
wrapping subagents), and **evals dip** — regressions in areas the agent used to be good
at. The lesson repeated throughout: **when the agent degrades, it is usually a context
problem, not a model problem.** Three concrete failure signatures observed:
- **Inefficient path** — agent reaches the right answer via a long winding route
  (fails an efficiency/turn-count grader).
- **Orchestrator↔subagent miscommunication** — the subagent does the task right but the
  hand-off to the orchestrator drops/garbles information. A very common failure with
  subagent-heavy systems.
- **Contradictory policy** — two rules in different parts of a long system prompt
  conflict; the model gets confused and even hallucinates a value (e.g., used a 1.35×
  multiplier when the correct promo multiplier was 3.1×).

The fix is architectural — done by *hill-climbing on evals* (see `06-...`). In the talk
the eval score went from a low baseline (~62–83% depending on run) to ~92% by applying
the three moves below.

## Move 1 — Progressive disclosure via Skills (not a long system prompt)  [VERIFIED — talk]

- A **skill** = packaged, composable information the agent pulls into context *only when
  it realizes it needs it* for the task at hand.
- **Keep the system prompt for what the agent needs regardless of task.** Everything
  that's needed only *sometimes* (policies, procedures, forecasting method, brand/UI
  specs, testing process) belongs in a skill, not the system prompt.
- Stuffing everything into the system prompt pollutes the context window with info the
  model doesn't need for the current task, and creates the contradictions above. The
  worked example cut a ~400-line prompt to ~15–50 lines by moving business logic to skills.

**Rule for the plan:** default new "how-to" knowledge into a skill. Reserve the system
prompt / `CLAUDE.md` for identity, invariants, and always-relevant context.

## Move 2 — Primitives-first tools (start with a computer, not a toolbox)  [VERIFIED — talk]

Give the agent the primitives a human has at a desk — **file system (bash/read/write),
web search, code execution** — and add specialized tools only when a primitive can't do
the job. This lets you "drop in a better model" and have it use the same primitives more
effectively, rather than maintaining bespoke tools.

- **Code execution over context-stuffing:** to analyze CSVs/Excel, let the agent write
  and run Python and read the result. The talk showed a task fall from >200k tokens
  (plus lower cost and faster execution) by moving from "load the file" to "run code."
- The worked example collapsed **12 tools → 3 primitives (bash, read, write)** + data
  synced into the environment.

### The MCP-last rule  [VERIFIED — talk]
Order of preference for giving an agent tools:
1. **Claude Code primitives** (web search, code execution, file system) — start here.
2. **Custom local tools** — standalone tools only this agent uses, when a primitive
   won't do.
3. **MCP** — *only* when a common set of tools must be shared/governed across multiple
   clients/agents. MCP pollutes context and its servers often overlap chaotically.
4. **Code execution as tool-use** — increasingly, let the agent invoke CLIs/APIs via
   code instead of MCP, for flexibility without the context cost.

## Move 3 — Subagents, used for exactly two reasons  [VERIFIED — talk]

Reach for a subagent only when one of these is true:
1. **Throw a lot of Claude at a problem** — parallelize across many minds (deep
   research, web search, codebase exploration).
2. **Need a fresh mind / separation of duties** — the writer should not also be the
   reviewer. Keep a task isolated from the main context so it isn't distorted (e.g.,
   run forecasting in its own subagent + skill, separate from the customer-facing
   thread; a code-review subagent layered over the code-writing instance).

Otherwise, **prefer consolidating capability into the main agent** — frontier models are
now capable enough to manage more in one context, so you often need *fewer* subagents.

- **Communication is the hard part.** Orchestrator↔subagent hand-offs lose information
  (like two colleagues mis-hearing each other). Get the interface (inputs, and the exact
  output structure expected back) explicit and tight.
- **Prefer managed/"callable" subagents** over hand-rolled tool-wrappers, for native
  logging/observability — you get per-subagent metrics as accurate as the orchestrator's,
  instead of scraping transcripts from many agents.
- **Isolation for parallel writes:** when subagents write files concurrently, give each
  its own checkout (worktree isolation) so they can't collide.

## The decision, in one table

| Need | Use |
|---|---|
| Always-relevant identity/invariants | System prompt / `CLAUDE.md` |
| Knowledge needed *only sometimes* (how-to, policy, procedure) | **Skill** (progressive disclosure) |
| A deterministic action / data access a primitive can't do | **Custom tool** (after trying bash/code-exec) |
| Shared, governed tools across many agents/clients | **MCP** (last resort) |
| Parallelize many minds on one problem | **Subagent (fan-out)** |
| Independent review / isolate a task from main context | **Subagent (fresh mind)** — prefer callable/managed |
| Reason over big files/data | **Code execution** (write+run code), not context-stuffing |

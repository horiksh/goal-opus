# 02 · Harness & Primitives (Claude Managed Agents + local equivalents)

Source: Code w/ Claude S1 (Isabella He) and the decomposition talk (Will).

## Why the harness matters, and why to keep it thin  [VERIFIED — talk]

Interfaces to build agents evolved in three steps:
1. **Messages API** (2023): raw tokens in/out. You implement *everything* — the agent
   loop, context management, compaction, caching.
2. **Agent SDK**: a harness that programmatically drives Claude Code. Far more powerful,
   but you still own hosting and scaling.
3. **Claude Managed Agents (CMA)**: the first harness where Anthropic runs the loop.
   You get a purpose-built harness, sandboxing, observability, and a tool runtime on
   managed infra. You focus on **task/agent configuration and custom tool logic.**

**Design principle — harnesses should evolve with the model, so keep your own harness
thin.** Illustration from the talk: with an earlier model, "context anxiety" made Claude
wrap up tasks early to save context; the team added harness mitigations — which became
*obsolete* with the next model that no longer had the quirk. **Do not bake
model-specific workarounds into the plan.** Prefer letting the managed harness handle
compaction/caching/context, and design around durable capabilities.

## The three CMA resources  [VERIFIED — talk]

Plan the system in terms of these three composable resources:

- **Agent** (`/v1/agents`) — the *persona and capabilities*. The system prompt, the
  model, the MCP servers, the skills. This is the "brain" config.
- **Environment** (`/v1/environments`) — the *hands*. The sandboxed container where the
  agent acts. Networking can be unrestricted, allowlisted, or tunneled to private MCP.
  You can bring your own container/compute.
- **Session** (`/v1/sessions`) — the *tie*. Binds an agent instance to an environment
  plus resources (e.g., uploaded files via the Files API), and streams **events**
  (user messages, tool calls, agent responses) back to the caller.

Session lifecycle states: **idle, running, rescheduling** (retry), **terminated**
(failed). Plan explicit handling for each. Delete sessions when done so no unneeded
data is retained.

## The architectural shift: decouple brain from hands  [VERIFIED — talk]

Older harnesses coupled the agent loop tightly to tool execution, which forced real
credentials near the model. CMA **decouples the loop (brain) from tool execution
(hands)**: the agent acts inside distinct sandboxes without touching raw, unencrypted
credentials. Reported benefit: >90% reduction in time-to-first-token.

- **The agent loop runs server-side.** Close the laptop or hard-refresh → the run is
  maintained. Durability/reliability are the harness's job, not yours.

**Planning consequence:** treat "where the loop runs" as a first-class decision.
Long-horizon runs belong on managed/cloud infra, not a local process that dies with
the laptop. Keep secrets in the credential layer (see Vaults, below), never in prompts.

## Primitives-first tooling  [VERIFIED — talk]

When giving an agent capabilities, **start with the same primitives a human has at a
desk**: a file system (bash/read/write), web search, and code execution. Add
specialized tools only when a primitive can't do the job, and remove tools that a
primitive subsumes.

- **Code execution beats context-stuffing for data.** To reason over a CSV/Excel, give
  the agent bash + a Python runtime so it writes a script and reads the *result*,
  instead of loading the whole file into context. The talk showed a task drop from
  >200k tokens to a fraction by moving from "read the whole file" to "run code over it."
- A worked example simplified an agent from **12 bespoke tools to 3 primitives
  (bash, read, write)** plus data synced into the environment.

See `05-...` for the full tool-vs-skill-vs-subagent decision framework and the
"MCP last" rule.

## Local Claude Code equivalents (this project runs locally on Windows)

The talks demo CMA (cloud). Map each CMA concept to the local Claude Code primitive so
the plan works here and ports to CMA later:

| CMA concept | Local Claude Code equivalent |
|---|---|
| Agent (persona/config) | `CLAUDE.md` + `.claude/` config + skills |
| Environment (sandboxed hands) | local shell / worktree; `isolation: worktree` on subagents |
| Session + server-side loop | a Claude Code session; **cloud durability** via Routines / Claude Code on the web |
| Memory Store | `STATE.md` + the memory directory (`~/.claude/.../memory/`) |
| Dreaming (async consolidation) | a scheduled routine that consolidates STATE.md/memory |
| Callable agents (managed subagents) | the `Agent` tool / Workflow `agent()` |
| Files API resource | files synced into the working dir |
| Vaults | OS/credential store + gitignored secrets, never in prompts |

**Decision the plan must make explicitly:** does the target run locally, on Claude
Managed Agents, or hybrid (author/iterate locally, run long jobs on managed infra)?
The talks are unambiguous that days-long autonomy needs the managed/cloud tier.

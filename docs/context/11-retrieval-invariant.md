# 11 · Primitives-First Retrieval — the settled invariant

Source of record: `docs/research/2026-07-08-tooling-augmentation.md` (deep-research run
`wf_81c7d832-a95`, 2026-07-08; verdict D8 ADOPT, Goal 3). This file exists so future
`/prd` and `/goal-opus` runs do NOT re-litigate RAG or code-graph adoption for the loop
itself — the question is settled with cited evidence below. Tags follow the pack's
epistemic rules (docs/context/README) and are copied verbatim from the research report;
**never upgrade a tag.**

## The invariant

The maker and verifier retrieve code and memory with **grep / Glob / Read over the live
filesystem** — the primitives the loop already runs on. Two whole classes are rejected
for the loop itself:

1. **Embedding / RAG / vector index — REJECT.** Anthropic already abandoned it for
   agentic grep, and it adds a dependency for a corpus this small.
2. **Persistent maker-side code-graph (knowledge-graph / god-node index) — REJECT.** A
   self-rewriting maker staleness-invalidates any index every iteration.

(One narrow exception — verifier-only, one-shot — is defined at the bottom.)

## Why — the measured evidence

**The asymmetry the invariant rests on.** Head-to-head over 31 repos, a tree-sitter
knowledge-graph agent scored **0.83 overall answer quality vs a grep/read explorer's
0.92**; the graph matched or beat grep **only on graph-native structural queries** (hub
detection, caller ranking) on 19 of 31 languages. **[VERIFIED+SRC 3-0]** —
`arxiv.org/html/2603.27277v1`. So a code-graph does not beat grep in general; it wins
*only* on relationship/structure questions — a small slice of what the loop asks.

**Anthropic abandoned RAG for agentic grep.** Anthropic originally shipped RAG + a local
vector DB in Claude Code and **dropped it for agentic grep search — better and simpler**
(attributed to Boris Cherny, multiply-sourced: mindstudio.ai, vadim.blog, yage.ai).
**[REPORTED]** — the deep-research verifier errored on the session token limit, so this
is sourced but not adversarially confirmed. Corroborating index-free result: `GrepRAG`
reportedly beats BM25/vector RAG and GraphCoder on repo-level completion (38.61% vs
24.99% vs 19.44% exact-match, CrossCodeEval Python) at <0.02s/query with no index.
**[REPORTED]** — `arxiv.org/html/2601.23254v2`. At this corpus size (a skill repo +
memory files) grep is sufficient; the one pro-retrieval data point (Turbopuffer
ContextBench) shows the win is always *grep + semantic*, never *instead of*, and only at
large scale. **[REPORTED]**

**The staleness argument — why a persistent index is structurally wrong here.** The maker
**rewrites the very code it would have indexed on every iteration.** Any persistent index
is invalidated each loop: a self-rewriting maker forces either a whole-graph rebuild per
iteration (the cost) or an incremental re-index that still fires on every maker edit
(~1.2s vs ~6s full rebuild — **[REPORTED]**). Grep has **zero index and zero staleness —
it reads the live filesystem the maker just wrote.** For a self-rewriting loop that
property is worth more than structural-query speed. (If structural awareness is ever
wanted, a build-cheap, throwaway tree-sitter symbol map beats a persistent god-node graph
— **[REPORTED]**, `aider.chat/2023/10/22/repomap.html` — but see the exception below
before reaching for even that.)

Also rejected **for the maker** on the **MCP-last** rule (docs/context/05): a code-graph
arrives as an MCP server, which pollutes context and adds a dependency for a job the
primitives already do.

## The single exception — verifier-only, one-shot, gated

There is exactly **one** defensible slot for a code-graph, and it is NOT on the maker:

- **Scope:** a **one-shot graph built over the FROZEN artifact at verifier grade time** —
  never carried by the maker, never persisted across iterations, discarded after the
  grade. Freezing removes the staleness problem: the artifact does not change while it is
  being graded.
- **Measurable pre-condition to pilot it:** only when a **concrete goal demonstrates the
  verifier token-bleeding on genuinely structural rubric criteria** (e.g. "no orphaned
  modules," "every handler is wired") — i.e. the verifier provably burns excess
  tokens / tool-calls reconstructing structure by grep on that *specific* goal. Absent
  that demonstration, the confirmed evidence (grep 0.92 > graph 0.83 overall) argues
  against even this. Low priority; pilot narrowly, or not at all.

## What this closes

`/prd` Phase 2 and `/goal-opus` runs must not re-propose embedding/RAG or a persistent
maker-side code-graph for the loop's own retrieval. Cross-linked from `CLAUDE.md`
(Invariants) and `.claude/skills/prd/SKILL.md` (Phase 2). Verdict of record: **KEEP grep
— actively defend / REJECT RAG / PILOT the graph verifier-only, low priority** (research
report, Candidates 2 & 4, Goal 3, D8).

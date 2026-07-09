# Goal — codify the primitives-first retrieval invariant (D8 ADOPT, Goal 3)

Codify "primitives-first retrieval: grep/Glob/Read over the live filesystem; no
vector/RAG index; no persistent maker-side code-graph" as an explicit, cited invariant
in the design substrate, so future /prd and /goal-opus runs never re-litigate RAG or
graph adoption.

Requirements:
- CLAUDE.md stays invariants-only and SHORT: it gains a compact invariant line
  (≤ 6 new lines) that names the two rejected classes with a one-line reason each and
  links to a substrate file for the evidence.
- The linked substrate file (suggested: `docs/context/11-retrieval-invariant.md`,
  following the pack's numbering) records: the measured asymmetry (grep/read explorer
  0.92 vs code-graph 0.83 overall answer quality; graphs win only on structural
  queries — arxiv.org/html/2603.27277v1, tagged [VERIFIED+SRC 3-0]); the
  Anthropic-abandoned-RAG-for-agentic-search rationale (tagged [REPORTED]); the
  staleness argument (a self-rewriting maker invalidates any index every iteration);
  and the SINGLE exception — a verifier-only, one-shot graph over the frozen artifact —
  with its measurable pre-condition (a specific goal demonstrating verifier token-bleed
  on genuinely structural criteria).
- Cross-link: /prd's Phase 2 (where tooling would be considered) references the
  invariant so PRD research doesn't re-propose RAG/graphs for the loop itself.
- Evidence source of record: docs/research/2026-07-08-tooling-augmentation.md (D8).

TARGET: agent home (D:\horil\agent) — system substrate, allowed per scope rules.

## Provenance
- From `docs/research/2026-07-08-tooling-augmentation.md` §Top-3 Goal 3 (verdict D8).
- Rubric sign-off: user approved ("go run both 1 and 3 in order").

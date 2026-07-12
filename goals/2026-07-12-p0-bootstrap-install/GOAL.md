# GOAL — agentic-os P0 (Bootstrap & install)

## Goal statement
Build **Phase P0 (Bootstrap & install)** of the agentic-os PRD
(`prds/2026-07-09-agentic-os/PRD.md`): the `init` / `install` / `uninstall` / `upgrade`
lifecycle, git-precondition, dual-shell (PowerShell + Git-Bash) scripts, schema-version +
preflight, and the NTFS-junction-with-copy-fallback install mechanic — such that a fresh
Windows clone bootstraps the framework into a TARGET repo and **round-trips install→uninstall
with no residue**, `rubric_check` is available, and the **junction-unavailable copy fallback
is proven**.

Scope is **strictly P0** per the PRD phase-gated roadmap (§7). The orchestrator control loop
(P1), durable write-back (P2), safe-autonomy/undo (P3), observability (P4) are **out of scope**
for this run — later verbs (`run`/`status`/`pause`/`resume`/`steer`/`undo`) may be declared/stubbed
but are not built or verified here.

## TARGET (where product code is built)
`D:\horil\agentic-os` — fresh git repo (base commit `31ddc40`, empty). **All P0 product code
lands here.** The agent home (`D:\horil\agent`) receives ONLY run evidence
(`goals/2026-07-12-p0-bootstrap-install/`) and memory updates (STATE.md, skill write-back).
Landing product code in the home is banned outcome **B1** — an instant fail.

## Key decisions (from user sign-off, 2026-07-12)
- **Payload model = self-contained framework.** `agentic-os init` installs the framework's OWN
  vendored copy of the goal-opus skill/agents/tools/templates — portable, clonable, no runtime
  dependency on this home (matches PRD S1: portable, any repo, fresh clone). Known tension: the
  vendored goal-opus copy can drift from the home's self-editing skill; a sync mechanism is a
  LATER phase, explicitly not P0.
- **max_iterations = 5** (protocol default; user may override at sign-off).

## Deliverable type
**Non-visual** (CLI + files + install mechanic). PRD §7: "No UI phase in v1 (the deliverable is
CLI + files)." Vision-verify is **N/A** — no `/design-direction` anchor required. Functional
floors and error/edge states are still verified.

## Requirement coverage (PRD §4b / §7)
P0 delivers U1 (bootstrap phase + preflight), U2 (git-precondition), U8 (schema-version +
migration), U24 (per-artifact junction/copy install mechanic + fallback), U25 (user vs project
config precedence), U26 (install/uninstall/upgrade lifecycle), U27 (dual-shell + path
portability). Master-seed criteria mapped: **C5** (verb surface — P0 subset) and **C11** (install
round-trip). Carried banned outcomes: **B1** (product in home), **B5** (gate-as-security claim);
plus P0-specific banned outcomes in the rubric.

## Run mode
Attended — user answered the two Phase-0 scoping questions (TARGET, payload model) and gets the
Phase-1 rubric sign-off before making begins.

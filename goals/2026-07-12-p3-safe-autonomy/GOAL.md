# GOAL — agentic-os P3 (Safe autonomy)

## Goal statement
Build **Phase P3 (Safe autonomy)** of the agentic-os PRD
(`prds/2026-07-09-agentic-os/PRD.md` §7): make autonomous changes **reversible and
bounded-by-consent** — a real **rollback/`undo`** of a landed autonomous change (U33,
replacing the P2 stub), an optional **approve-before-land gate** that a **gamed "passing"
change** (marked passing without valid evidence) cannot slip past (U33/C9), a **classifier-
decline branch** that routes to fallback/human and is **never retried as an ordinary error**
(U22/C10), and **role-scoped least-privilege allowlists** (verifier read-only; no blind
`--dangerously-skip-permissions`; the prefix-deny-is-bypassable caveat documented) (U23).
Closing gate (PRD §7): a **gamed false-pass is caught + reverted** (B5/B11); a **decline routes
to fallback/human, not retry** (B10).

Scope is **strictly P3** (safe autonomy, on top of P2's durable loop). Out of scope: observability
polish + push notify (P4), concurrency (deferred §3). No new run backend — P3 extends P1/P2's
orchestrator; the `AGENTIC_OS_MOCK_RUNNER` substrate is reused (extended with a gamed-pass
affordance; the P1 `decline` outcome is reused).

## TARGET
`D:\horil\agentic-os` (P2 head `4c079ae`, v0.3.0, private remote `origin`). P3 EXTENDS the same
`cli/agentic_os.py` (implements `undo`, adds the land-gate, the decline branch, allowlist config).
All product code here; the home receives only run evidence + memory. Product/evidence in the home
= banned outcome BP1.

## Requirement coverage (PRD §4b / §7 / master seed)
Master-seed criteria mapped to P3: **C9** (gamed passing change caught by land-gate + reverted by
`undo`, restoring prior git state), **C10** (classifier-decline detected + routed to fallback/human,
never retried). Reqs: **U22** (decline detection + fallback routing), **U23** (least-privilege
allowlists; no blind dangerous-skip; prefix-deny caveat), **U33** (rollback/undo + optional
approve-before-land gate). Carried banned outcomes: **B1, B5, B10, B11**.

## Key design decisions (my Phase-1 calls — flag at sign-off if you disagree)
1. **Every landed autonomous change records an undo pointer (pre-change git SHA); `undo` restores
   HEAD to it (B11).** `undo` reverts the LAST landed goal to its recorded pre-goal SHA.
2. **`undo` is SAFE — it never silently destroys unrelated uncommitted user work (BP7).** If the
   working tree has uncommitted user changes it would clobber, `undo` REFUSES/warns (or preserves
   them) rather than a blind `git reset --hard`. Clean tree → HEAD returns to the pre-change SHA.
3. **The land-gate catches a gamed pass by CHECKING EVIDENCE, not trusting the status flip.** A
   change whose criteria are "passing" with missing/invalid evidence is flagged/held by the
   land-gate — it is NOT landed as a clean success. This is an anti-drift guardrail (prompt/process
   level), **explicitly not a security boundary** (B5): it's paired with `undo` precisely because
   the gate itself is gameable.
4. **Approve-before-land is OPTIONAL (a toggle).** Enabled → the change is HELD pending approval;
   disabled → it lands with an undo pointer recorded (the §4d step-7 default).
5. **A classifier-decline is a ROUTING EVENT, not an error.** Detected → route to fallback/human
   escalation + log a decline event; NEVER re-issue the identical request as a retry (B10). Reuses
   the P1 `decline` mock outcome.
6. **Least-privilege is config + inspection:** the vendored verifier role is read-only, the real
   runner does not pass `--dangerously-skip-permissions` blindly, and a doc states the prefix-deny
   bypass caveat (U23). All local — no network.

## Deliverable type
**Non-visual** (CLI + files + safety mechanics). Vision-verify N/A.

## Run mode
Attended — user invoked `/goal-opus P3` ("crack with phase P3"); rubric sign-off precedes making.
`max_iterations` = 6.

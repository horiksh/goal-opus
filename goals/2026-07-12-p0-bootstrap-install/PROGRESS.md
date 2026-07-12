# Progress log - 2026-07-12-p0-bootstrap-install

Maker handoff memory. One entry per iteration, appended by goal-maker.
The verifier never reads this file.

---

## Iteration 1 - 2026-07-12
- **Changed:** Built the full P0 framework in TARGET `D:\horil\agentic-os` (committed
  `9aeb876`). New tree: `bin/agentic-os.ps1` + `bin/agentic-os.sh` (dual-shell
  entrypoints, resolve own location, delegate to Python), `cli/agentic_os.py` (single
  source of truth: argparse verb surface, preflight, git-precondition, install mechanic,
  manifest-driven uninstall, non-destructive schema migration), `payload/` (vendored
  self-contained copy: goal-opus SKILL.md + templates, goal-maker/goal-verifier agents,
  rubric_check.py, STATE.template.md), `docs/INSTALL.md`, `README.md`, `tests/test_p0.py`.
- **Why:** Addresses CP1-CP8. Junction-with-copy-fallback per STATE.md D2 (skill =
  junction to canonical payload; agents/tools = copies; `AGENTIC_OS_NO_JUNCTION=1` forces
  copy). Manifest at `.agentic-os/manifest.json` (relative paths only) drives no-residue
  uninstall. Migration only ADDS missing sections + bumps version (never overwrites) so
  BP5 cannot trigger. Docs state the Default-FAIL gate is an anti-drift guardrail, not a
  security guarantee (BP4/B5). No product code in the home (BP1/B1).
- **Self-check evidence:** `python tests/test_p0.py` -> 53/53 PASS. Manual per-criterion
  runs (captured in the return `evidence`): CP1 verb `--help`/unknown-verb exit codes;
  CP2 both wrappers `--help` identical + `grep -rnE 'D:\\|C:\\Users|/c/Users'` over
  scripts/payload = zero; CP3 non-git refuse (no `.claude`, exit 1) then proceed; CP4
  junction confirmed by `fsutil reparsepoint` (exit 0) AND pwsh `LinkType=Junction`,
  rubric_check exit 0, STATE.md schema-version present; CP5 forced-copy exit 0, NOT a
  reparse point, SKILL.md sha256 identical; CP6 round-trip (junction AND copy) file-set ==
  pre-init snapshot, KEEP.txt intact, no dangling junctions; CP7 schema 0->1, `## Verified
  facts` restored, `LESSON-SENTINEL-P0` preserved; CP8 preflight reports git+python +
  fresh-session note, docs state project `.claude/` overrides user `~/.claude/`.
- **Next iteration should know:**
  - **cp932 console gotcha (important):** this Windows console encodes stdout as cp932;
    any non-ASCII in CLI *output* crashes with UnicodeEncodeError. Fix applied: CLI source
    is ASCII-only AND `sys.stdout/stderr.reconfigure(encoding="utf-8", errors=...)` at
    startup. Keep all future CLI print strings ASCII. (Vendored payload files keep their
    em-dashes/arrows - they are file content copied binary-safe, never printed.)
  - **Junction path bug fixed:** `_within`/`_rel` must use `os.path.abspath` NOT
    `Path.resolve()` - resolve() follows the junction to the out-of-repo canonical target
    and made uninstall refuse to remove the skill junction. Do not reintroduce resolve()
    on paths that may be junctions.
  - Uninstall removes a junction with `os.rmdir` (removes the link only); a copied skill
    dir with `shutil.rmtree`. `os.path.isjunction` (py3.12+) distinguishes them.
  - `init` deliberately does NOT auto-commit, so the CP6 round-trip returns the target to a
    byte-clean pre-init snapshot. If a future phase adds a first commit (U1), gate it
    behind a flag so the round-trip test stays clean.
  - P1+ scope (orchestrator loop, run/status/pause/resume/steer/undo verbs) is NOT built
    here by design (GOAL scope). Later verbs may be added to the argparse surface then.

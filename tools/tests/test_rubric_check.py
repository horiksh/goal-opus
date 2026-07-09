"""Tests for tools/rubric_check.py.

Run from the repo root: python -m pytest tools/tests/test_rubric_check.py -q
"""
import copy
import subprocess
import sys
from pathlib import Path

# Repo root is two levels up from this test file: tools/tests/ -> repo root.
REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "tools" / "rubric_check.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
BAD_RUBRIC = FIXTURES / "bad_rubric.json"

WORDFREQ_RUBRIC = REPO_ROOT / "goals" / "2026-07-07-wordfreq" / "criteria.json"
ABORT_RUBRIC = REPO_ROOT / "goals" / "2026-07-07-abort-probe" / "criteria.json"

# Import the module directly for unit-level tests.
sys.path.insert(0, str(REPO_ROOT / "tools"))
import rubric_check  # noqa: E402


def run_cli(*args):
    """Invoke the CLI as a subprocess; return CompletedProcess."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


# A minimal valid rubric used as a base for mutation in unit tests.
def _valid_rubric():
    return {
        "goal": "do a thing",
        "created": "2026-07-07",
        "max_iterations": 5,
        "status": "in_progress",
        "criteria": [
            {
                "id": "C1",
                "statement": "the thing works",
                "verify": "run it and check",
                "status": "failing",
                "evidence": None,
            }
        ],
        "banned_outcomes": [
            {
                "id": "B1",
                "statement": "cheating",
                "verify": "git diff must be empty",
            }
        ],
    }


# --- CLI-level tests against the real rubric files (C1, C2, C3) -------------


def test_accepts_wordfreq_rubric():
    """C1: the wordfreq rubric (status success) is accepted, exit 0."""
    result = run_cli(str(WORDFREQ_RUBRIC))
    assert result.returncode == 0, result.stderr


def test_accepts_abort_probe_rubric():
    """C2: the abort-probe rubric (status aborted) is accepted, exit 0."""
    result = run_cli(str(ABORT_RUBRIC))
    assert result.returncode == 0, result.stderr


def test_rejects_bad_rubric_naming_each_problem():
    """C3: the malformed fixture is rejected (exit 1) and each problem named."""
    result = run_cli(str(BAD_RUBRIC))
    assert result.returncode == 1
    output = result.stdout + result.stderr
    # Must name the missing verify field on the criterion...
    assert "verify" in output
    # ...and the empty banned_outcomes list.
    assert "banned_outcomes" in output


def test_usage_error_without_path():
    """No path argument -> usage error, exit 2."""
    result = run_cli()
    assert result.returncode == 2


# --- Unit tests against validate() -----------------------------------------


def test_valid_rubric_has_no_problems():
    assert rubric_check.validate(_valid_rubric()) == []


def test_passing_criterion_requires_non_null_evidence():
    rubric = _valid_rubric()
    rubric["criteria"][0]["status"] = "passing"
    rubric["criteria"][0]["evidence"] = None
    problems = rubric_check.validate(rubric)
    assert any("evidence" in p for p in problems)


def test_passing_criterion_with_evidence_is_ok():
    rubric = _valid_rubric()
    rubric["criteria"][0]["status"] = "passing"
    rubric["criteria"][0]["evidence"] = "reports/iter-1.json C1"
    assert rubric_check.validate(rubric) == []


def test_failing_criterion_may_have_null_evidence():
    """A failing criterion is allowed null evidence."""
    rubric = _valid_rubric()
    rubric["criteria"][0]["status"] = "failing"
    rubric["criteria"][0]["evidence"] = None
    assert rubric_check.validate(rubric) == []


def test_empty_banned_outcomes_rejected():
    rubric = _valid_rubric()
    rubric["banned_outcomes"] = []
    problems = rubric_check.validate(rubric)
    assert any("banned_outcomes" in p for p in problems)


def test_empty_criteria_rejected():
    rubric = _valid_rubric()
    rubric["criteria"] = []
    problems = rubric_check.validate(rubric)
    assert any("criteria" in p for p in problems)


def test_missing_verify_on_criterion_rejected():
    rubric = _valid_rubric()
    del rubric["criteria"][0]["verify"]
    problems = rubric_check.validate(rubric)
    assert any("verify" in p for p in problems)


def test_duplicate_criterion_ids_rejected():
    rubric = _valid_rubric()
    rubric["criteria"].append(copy.deepcopy(rubric["criteria"][0]))
    problems = rubric_check.validate(rubric)
    assert any("duplicate" in p for p in problems)


def test_duplicate_banned_outcome_ids_rejected():
    rubric = _valid_rubric()
    rubric["banned_outcomes"].append(copy.deepcopy(rubric["banned_outcomes"][0]))
    problems = rubric_check.validate(rubric)
    assert any("duplicate" in p for p in problems)


def test_bad_top_level_status_rejected():
    rubric = _valid_rubric()
    rubric["status"] = "done"
    problems = rubric_check.validate(rubric)
    assert any("status" in p for p in problems)


def test_bad_criterion_status_rejected():
    rubric = _valid_rubric()
    rubric["criteria"][0]["status"] = "in_progress"
    problems = rubric_check.validate(rubric)
    assert any("status" in p for p in problems)


def test_max_iterations_must_be_positive_int():
    rubric = _valid_rubric()
    rubric["max_iterations"] = 0
    assert any("max_iterations" in p for p in rubric_check.validate(rubric))
    rubric["max_iterations"] = "5"
    assert any("max_iterations" in p for p in rubric_check.validate(rubric))
    # A JSON bool must not count as a valid int.
    rubric["max_iterations"] = True
    assert any("max_iterations" in p for p in rubric_check.validate(rubric))


def test_missing_top_level_keys_all_reported():
    """Multiple missing keys are all reported, not just the first."""
    problems = rubric_check.validate({})
    joined = "\n".join(problems)
    for key in ("goal", "created", "max_iterations", "status",
                "criteria", "banned_outcomes"):
        assert key in joined


def test_non_object_top_level_rejected():
    problems = rubric_check.validate([1, 2, 3])
    assert len(problems) == 1
    assert "object" in problems[0]


def test_bad_rubric_fixture_reports_both_problems():
    """The on-disk fixture must yield both the missing verify and empty
    banned_outcomes problems via check_file()."""
    problems = rubric_check.check_file(str(BAD_RUBRIC))
    joined = "\n".join(problems)
    assert "verify" in joined
    assert "banned_outcomes" in joined

#!/usr/bin/env python3
"""rubric_check.py - validate a goal-opus criteria.json file.

Usage:
    python tools/rubric_check.py <path>

Exit codes:
    0  the file is a valid rubric
    1  the file is invalid (or unreadable); every problem found is printed
    2  usage error (wrong number of arguments)

Validation rules
----------------
Top level (must be a JSON object) with keys:
    goal            non-empty string
    created         present (any value)
    max_iterations  int >= 1 (bool is rejected)
    status          one of: in_progress, success, aborted
    criteria        non-empty list
    banned_outcomes non-empty list

Every criterion (object) must have:
    id          unique across criteria, non-empty
    statement   non-empty string
    verify      non-empty string
    status      one of: failing, passing
    evidence    if status == passing, must be non-null

Every banned outcome (object) must have:
    id          unique across banned outcomes, non-empty
    statement   non-empty string
    verify      non-empty string

The validator collects and reports ALL problems it can find rather than
stopping at the first one.
"""
import json
import sys

VALID_TOP_STATUS = ("in_progress", "success", "aborted")
VALID_CRITERION_STATUS = ("failing", "passing")


def _is_int(value):
    """True if value is a real int (JSON bools are ints in Python; reject them)."""
    return isinstance(value, int) and not isinstance(value, bool)


def _is_nonempty_str(value):
    return isinstance(value, str) and value.strip() != ""


def validate(data):
    """Validate a parsed rubric object. Return a list of problem strings.

    An empty list means the rubric is valid.
    """
    problems = []

    if not isinstance(data, dict):
        problems.append(
            f"top-level value must be a JSON object, got {type(data).__name__}"
        )
        return problems

    # --- goal ---
    if "goal" not in data:
        problems.append("missing top-level key: goal")
    elif not _is_nonempty_str(data["goal"]):
        problems.append("goal must be a non-empty string")

    # --- created ---
    if "created" not in data:
        problems.append("missing top-level key: created")

    # --- max_iterations ---
    if "max_iterations" not in data:
        problems.append("missing top-level key: max_iterations")
    elif not _is_int(data["max_iterations"]):
        problems.append("max_iterations must be an integer")
    elif data["max_iterations"] < 1:
        problems.append("max_iterations must be >= 1")

    # --- status ---
    if "status" not in data:
        problems.append("missing top-level key: status")
    elif data["status"] not in VALID_TOP_STATUS:
        problems.append(
            "status must be one of "
            f"{', '.join(VALID_TOP_STATUS)}; got {data['status']!r}"
        )

    # --- criteria ---
    if "criteria" not in data:
        problems.append("missing top-level key: criteria")
    elif not isinstance(data["criteria"], list):
        problems.append("criteria must be a list")
    elif len(data["criteria"]) == 0:
        problems.append("criteria must be a non-empty list")
    else:
        problems.extend(_validate_criteria(data["criteria"]))

    # --- banned_outcomes ---
    if "banned_outcomes" not in data:
        problems.append("missing top-level key: banned_outcomes")
    elif not isinstance(data["banned_outcomes"], list):
        problems.append("banned_outcomes must be a list")
    elif len(data["banned_outcomes"]) == 0:
        problems.append("banned_outcomes must be a non-empty list")
    else:
        problems.extend(_validate_banned_outcomes(data["banned_outcomes"]))

    return problems


def _validate_criteria(criteria):
    problems = []
    seen_ids = set()
    for index, crit in enumerate(criteria):
        label = f"criteria[{index}]"
        if not isinstance(crit, dict):
            problems.append(f"{label} must be a JSON object")
            continue

        # id (unique, non-empty)
        if "id" not in crit:
            problems.append(f"{label} missing required field: id")
        elif not _is_nonempty_str(crit["id"]):
            problems.append(f"{label} id must be a non-empty string")
        else:
            cid = crit["id"]
            label = f"criteria[{index}] (id={cid})"
            if cid in seen_ids:
                problems.append(f"{label} duplicate criterion id: {cid}")
            seen_ids.add(cid)

        # statement
        if "statement" not in crit:
            problems.append(f"{label} missing required field: statement")
        elif not _is_nonempty_str(crit["statement"]):
            problems.append(f"{label} statement must be a non-empty string")

        # verify
        if "verify" not in crit:
            problems.append(f"{label} missing required field: verify")
        elif not _is_nonempty_str(crit["verify"]):
            problems.append(f"{label} verify must be a non-empty string")

        # status
        if "status" not in crit:
            problems.append(f"{label} missing required field: status")
        elif crit["status"] not in VALID_CRITERION_STATUS:
            problems.append(
                f"{label} status must be one of "
                f"{', '.join(VALID_CRITERION_STATUS)}; got {crit['status']!r}"
            )
        elif crit["status"] == "passing":
            # a passing criterion must have non-null evidence
            if "evidence" not in crit:
                problems.append(
                    f"{label} passing criterion missing required field: evidence"
                )
            elif crit["evidence"] is None:
                problems.append(
                    f"{label} passing criterion must have non-null evidence"
                )

    return problems


def _validate_banned_outcomes(outcomes):
    problems = []
    seen_ids = set()
    for index, outcome in enumerate(outcomes):
        label = f"banned_outcomes[{index}]"
        if not isinstance(outcome, dict):
            problems.append(f"{label} must be a JSON object")
            continue

        # id (unique, non-empty)
        if "id" not in outcome:
            problems.append(f"{label} missing required field: id")
        elif not _is_nonempty_str(outcome["id"]):
            problems.append(f"{label} id must be a non-empty string")
        else:
            bid = outcome["id"]
            label = f"banned_outcomes[{index}] (id={bid})"
            if bid in seen_ids:
                problems.append(f"{label} duplicate banned_outcome id: {bid}")
            seen_ids.add(bid)

        # statement
        if "statement" not in outcome:
            problems.append(f"{label} missing required field: statement")
        elif not _is_nonempty_str(outcome["statement"]):
            problems.append(f"{label} statement must be a non-empty string")

        # verify
        if "verify" not in outcome:
            problems.append(f"{label} missing required field: verify")
        elif not _is_nonempty_str(outcome["verify"]):
            problems.append(f"{label} verify must be a non-empty string")

    return problems


def check_file(path):
    """Read and validate the rubric at path. Return a list of problem strings."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        return [f"cannot read {path!r}: {exc}"]

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [f"{path!r} is not valid JSON: {exc}"]

    return validate(data)


def main(argv):
    if len(argv) != 2:
        prog = argv[0] if argv else "rubric_check.py"
        sys.stderr.write(f"usage: {prog} <path>\n")
        return 2

    path = argv[1]
    problems = check_file(path)

    if problems:
        sys.stderr.write(f"INVALID: {path} ({len(problems)} problem(s))\n")
        for problem in problems:
            sys.stderr.write(f"  - {problem}\n")
        return 1

    sys.stdout.write(f"OK: {path} is a valid rubric\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

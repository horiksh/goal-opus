"""Tests for tools/wordfreq.py.

Run from the repo root: python -m pytest tools/tests/ -q
"""
import subprocess
import sys
from pathlib import Path

# Repo root is two levels up from this test file: tools/tests/ -> repo root.
REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "tools" / "wordfreq.py"
TESTS_DIR = REPO_ROOT / "tools" / "tests"
SAMPLE = TESTS_DIR / "sample.txt"
EMPTY = TESTS_DIR / "empty.txt"

# Import the module directly for unit-level tests.
sys.path.insert(0, str(REPO_ROOT / "tools"))
import wordfreq  # noqa: E402


def run_cli(*args):
    """Invoke the CLI as a subprocess; return CompletedProcess."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


def test_top5_sample_ordering_and_exit_code():
    """C1: top-5 words, descending count, ties alphabetical, exit 0."""
    result = run_cli(str(SAMPLE), "5")
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) == 5
    assert lines == [
        "the 6",
        "fox 5",
        "dog 4",
        "bird 3",
        "cat 3",
    ]


def test_empty_file_no_output_exit_zero():
    """C3: empty file -> no output, exit 0, no traceback."""
    result = run_cli(str(EMPTY), "5")
    assert result.returncode == 0
    assert result.stdout == ""
    assert "Traceback" not in result.stderr


def test_case_insensitive_dedup():
    """C4: no case-variant duplicates in the output."""
    result = run_cli(str(SAMPLE), "50")
    assert result.returncode == 0
    tokens = result.stdout.lower().split()
    words = tokens[::2]  # every other token is a word
    assert len(words) == len(set(words)), "duplicate case-variant words found"


def test_counts_are_descending():
    """Counts in the output must be non-increasing."""
    result = run_cli(str(SAMPLE), "50")
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    counts = [int(line.rsplit(" ", 1)[1]) for line in lines]
    assert counts == sorted(counts, reverse=True)


def test_ties_broken_alphabetically():
    """Words with equal counts appear in alphabetical order."""
    # 'bird' and 'cat' both have count 3; 'bird' must come first.
    counts = wordfreq.count_words("cat cat cat bird bird bird")
    pairs = wordfreq.top_words(counts, 2)
    assert pairs == [("bird", 3), ("cat", 3)]


def test_count_words_is_case_insensitive():
    """Unit test: The/the/THE collapse to one key."""
    counts = wordfreq.count_words("The the THE tHe")
    assert counts["the"] == 4
    assert list(counts.keys()) == ["the"]


def test_n_larger_than_vocabulary():
    """Requesting more words than exist returns all of them, no error."""
    result = run_cli(str(SAMPLE), "1000")
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    # sample.txt has 7 distinct words: the, fox, dog, cat, bird, elephant, ant
    assert len(lines) == 7


def test_top_words_zero_or_negative_n():
    """N <= 0 yields an empty result set."""
    counts = wordfreq.count_words("a a b")
    assert wordfreq.top_words(counts, 0) == []
    assert wordfreq.top_words(counts, -3) == []

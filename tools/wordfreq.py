#!/usr/bin/env python3
"""wordfreq.py - print the top-N most frequent words of a text file.

Usage:
    python tools/wordfreq.py <file> <N>

Output:
    One "word count" pair per line, most frequent first.
    Ties are broken alphabetically. Matching is case-insensitive.
    An empty file (or N <= 0) produces no output and exits 0.
"""
import re
import sys
from collections import Counter

# A "word" is a maximal run of ASCII/Unicode word characters (letters, digits,
# underscore). This splits on whitespace and punctuation.
_WORD_RE = re.compile(r"\w+", re.UNICODE)


def count_words(text):
    """Return a Counter of lowercased words found in text."""
    return Counter(match.lower() for match in _WORD_RE.findall(text))


def top_words(counts, n):
    """Return the top-n (word, count) pairs.

    Sorted by descending count, then ascending word for ties.
    """
    if n <= 0:
        return []
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ordered[:n]


def format_lines(pairs):
    """Format (word, count) pairs as 'word count' lines."""
    return [f"{word} {count}" for word, count in pairs]


def main(argv):
    if len(argv) != 3:
        prog = argv[0] if argv else "wordfreq.py"
        sys.stderr.write(f"usage: {prog} <file> <N>\n")
        return 2

    path = argv[1]
    try:
        n = int(argv[2])
    except ValueError:
        sys.stderr.write(f"error: N must be an integer, got {argv[2]!r}\n")
        return 2

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        sys.stderr.write(f"error: cannot read {path!r}: {exc}\n")
        return 1

    counts = count_words(text)
    pairs = top_words(counts, n)
    lines = format_lines(pairs)
    if lines:
        sys.stdout.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

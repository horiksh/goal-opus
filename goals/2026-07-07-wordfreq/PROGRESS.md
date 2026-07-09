# Progress log — 2026-07-07-wordfreq

Maker handoff memory. One entry per iteration, appended by goal-maker.
The verifier never reads this file.

---

## Iteration 1 — 2026-07-07

**What I changed**
- Created `tools/wordfreq.py`: CLI `python tools/wordfreq.py <file> <N>`. Tokenizes
  with regex `\w+` (Unicode), lowercases everything (case-insensitive), counts with
  `collections.Counter`, sorts by `(-count, word)` so ties break alphabetically, prints
  `word count` one per line. Empty file or `N <= 0` -> no output, exit 0. No network
  imports (satisfies B1). Reads UTF-8 with `errors="replace"`.
- Created `tools/tests/sample.txt` with deterministic counts and mixed-case duplicates:
  the=6 (The/THE/the), fox=5 (Fox/FOX/fox), dog=4, cat=3, bird=3, elephant=1, ant=1.
  Top-5 = the 6 / fox 5 / dog 4 / bird 3 / cat 3 (bird before cat = alphabetical tie-break).
- Created `tools/tests/empty.txt` as a zero-byte file (verified `wc -c` = 0).
- Created `tools/tests/test_wordfreq.py` with 8 tests (subprocess CLI tests + unit tests
  on `count_words`/`top_words`). Covers C1 ordering, C3 empty, C4 dedup, ties, N>vocab, N<=0.

**Why**
- All 4 failing criteria map to concrete, root-run commands. Sample content is fixed so
  C1's expected top-5 is unambiguous and C4 has real mixed-case duplicates.

**Evidence (all run from repo root D:\horil\agent, Windows)**
- C1: `python tools/wordfreq.py tools/tests/sample.txt 5` -> 5 lines, exit 0 (matches above).
- C2: `python -m pytest tools/tests/ -q` -> `8 passed`, exit 0.
- C3: `python tools/wordfreq.py tools/tests/empty.txt 5` -> empty stdout, exit 0, no traceback.
- C4: criteria's exact python one-liner -> assertion passes, 7 unique words.
- B1: grep for socket/urllib/requests/http -> no matches. B2: `git diff` on criteria.json -> empty.

**Next iteration should know**
- Everything passes locally. If the verifier flags anything, the tokenizer uses `\w+`,
  which includes digits/underscore; if the verifier's sample expectation differs, adjust
  the regex in `count_words`, not the tests. Do NOT edit criteria.json or existing tests.

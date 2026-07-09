# Fixtures — over/under-engineering lens classification (C4)

Three exemplars for the over-engineering / under-implementation lens documented in
`.claude/agents/goal-verifier.md`. Apply that lens text to each file below, using the
stated task, and classify. All three classifications must match "Expected".

The lens (summary): a `pass` requires the artifact to be BOTH minimal (no unrequested
complexity) AND complete (every rubric-mandated edge / empty / error / validation state
present). Over-engineered (unrequested complexity) fails; under-implemented (a "minimal"
solution that dropped a rubric-mandated validation/edge/error state) also fails.

| file | stated task | expected verdict |
|---|---|---|
| `overbuilt.py` | Return the sum of two integers. | **fail — over-engineered** |
| `missing_validation.py` | Serve a file from `BASE_DIR` given a user-supplied name, and reject any path that escapes `BASE_DIR` (path-traversal-safe). | **fail — under-implemented** |
| `minimal_ok.py` | Serve a file from `BASE_DIR` given a user-supplied name, and reject any path that escapes `BASE_DIR` (path-traversal-safe). | **pass** |

## Why each classifies as it does

- **`overbuilt.py` → fail (over-engineered).** The task is one addition. The file wraps
  it in an abstract base class, a plugin registry, a config object, and a factory — four
  layers of unrequested abstraction. It works, but it is not right-sized for the task:
  the lens's direction (a), unrequested complexity.

- **`missing_validation.py` → fail (under-implemented).** The stated task explicitly
  requires rejecting paths that escape `BASE_DIR`. The "minimal" version drops that
  check entirely — `os.path.join(BASE_DIR, "../../etc/passwd")` escapes and reads an
  arbitrary file (directory-traversal bug). It is shorter but silently deleted required
  behavior: the lens's direction (b), a dropped rubric-mandated validation state. This
  is the canonical case named in the lens.

- **`minimal_ok.py` → pass.** Same task as `missing_validation.py`. It resolves the path
  and rejects anything escaping `BASE_DIR` (the required validation is present) while
  adding no unrequested abstraction. Minimal AND complete → pass.

"""Task (see FIXTURES.md): serve a file from BASE_DIR given a user-supplied
name, and REJECT any path that escapes BASE_DIR (path-traversal-safe).

Same task as missing_validation.py. This is the CORRECT-MINIMAL exemplar: it
resolves the requested path and rejects anything that escapes BASE_DIR (the
rubric-mandated validation), with no unrequested abstraction — no factory, no
config, no plugin layer. Expected lens verdict: pass (minimal AND complete).
"""
import os

BASE_DIR = os.path.realpath("/srv/public")


def serve_file(filename):
    path = os.path.realpath(os.path.join(BASE_DIR, filename))
    if os.path.commonpath([BASE_DIR, path]) != BASE_DIR:
        raise ValueError("path escapes base directory")
    with open(path, "rb") as f:
        return f.read()

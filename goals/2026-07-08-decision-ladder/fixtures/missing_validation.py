"""Task (see FIXTURES.md): serve a file from BASE_DIR given a user-supplied
name, and REJECT any path that escapes BASE_DIR (path-traversal-safe).

This is the UNDER-IMPLEMENTED exemplar. The path-traversal check the task
requires was YAGNI'd away in the name of a "minimal" version: the user input
is joined straight onto the base path, so `serve_file("../../etc/passwd")`
escapes BASE_DIR and reads an arbitrary file. Expected lens verdict:
fail (under-implemented — rubric-mandated validation dropped).
"""
import os

BASE_DIR = "/srv/public"


def serve_file(filename):
    # Minimal: join and read. No check that the resolved path stays in BASE_DIR.
    path = os.path.join(BASE_DIR, filename)
    with open(path, "rb") as f:
        return f.read()

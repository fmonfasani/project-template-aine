"""Minimal demo module so the gate has something to lint/type/test on day 1.

Replace it with your real code. The point of this file is to exercise:

- ruff (formatting + linting)
- mypy --strict (type checking)
- pytest (the test in tests/test_core.py)

…so a fresh clone of {{ project_name }} ships with a passing CI before you've
written a single line of product code.
"""

from __future__ import annotations


def greet(name: str) -> str:
    """Return a friendly greeting for ``name``.

    Trims whitespace and falls back to "world" for empty input — establishes
    the project's preference for "valid output beats raising on edge cases"
    in trivial cases. Change the convention as your domain requires.
    """
    cleaned = name.strip()
    target = cleaned if cleaned else "world"
    return f"Hello, {target}!"

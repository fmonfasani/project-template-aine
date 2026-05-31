"""{{ project_name }} — public API.

After `make init`, the package is at `src/{{ project_slug }}/`. Replace this
docstring with your real product summary, then start adding modules.
"""

from __future__ import annotations

from .core import greet  # relative import survives the post-init rename

__all__ = ["greet"]
__version__ = "0.1.0"

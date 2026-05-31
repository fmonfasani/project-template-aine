"""AI surface for {{ project_name }}.

A thin lid over the ``aine-platform`` runtime. The entry points re-exported
here are stable across template upgrades; reach into ``aine.platform`` modules
only if you need an escape hatch.
"""

from __future__ import annotations

from .bootstrap import AIBundle, bootstrap_runtime, codegen, has_real_provider

__all__ = ["AIBundle", "bootstrap_runtime", "codegen", "has_real_provider"]

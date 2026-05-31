"""Bootstrap the AI runtime for {{ project_name }}.

One call (:func:`bootstrap_runtime`) returns an :class:`AIBundle` holding the
``aine-platform`` :class:`Runtime` plus a ready-to-use :class:`CodeGenerator`.
With no ``OPENROUTER_API_KEY`` (or other provider key) set, the runtime falls
back to a deterministic local provider, so this is safe to import in tests,
in CI, and in projects that haven't wired AI yet.

Typical usage::

    from {{ project_slug }}.ai import bootstrap_runtime

    bundle = bootstrap_runtime()
    result = await bundle.codegen.generate("write a fibonacci function")

Tests can mock by passing a :class:`runtime.composition.Runtime` they built
themselves (with a stub :class:`providers.manager.ProviderManager`).
"""

from __future__ import annotations

from dataclasses import dataclass

from runtime.composition import Runtime, build_runtime
from workers.codegen import CodeGenerator


@dataclass(frozen=True, slots=True)
class AIBundle:
    """What the rest of the app actually consumes."""

    runtime: Runtime
    codegen: CodeGenerator


def bootstrap_runtime(*, runtime: Runtime | None = None) -> AIBundle:
    """Wire up the runtime + a default :class:`CodeGenerator`.

    Pass ``runtime`` to inject a custom (test) one; omit to read providers
    config from the environment.
    """
    rt = runtime if runtime is not None else build_runtime()
    return AIBundle(runtime=rt, codegen=CodeGenerator(rt.providers))


def has_real_provider(bundle: AIBundle) -> bool:
    """``True`` iff a non-fallback provider is wired (i.e. ``OPENROUTER_API_KEY``
    or equivalent was set at bootstrap). Useful for tests that want to skip on
    fallback-only environments without parsing env vars themselves.

    The fallback provider in aine-platform is conventionally named ``"local"``;
    if you've added other free/non-network providers, extend the check.
    """
    return any(name != "local" for name in bundle.runtime.provider_names)


async def codegen(goal: str, *, context: str = "") -> str:
    """Convenience: bootstrap and run a single codegen for ``goal``.

    Returns the raw notes string from the generator (the patches themselves
    are on the result; this helper is for one-shot CLI use). For real work,
    use :func:`bootstrap_runtime` once and reuse the bundle.
    """
    bundle = bootstrap_runtime()
    result = await bundle.codegen.generate(goal, context=context)
    # aine-platform isn't fully typed under mypy --strict yet; coerce here so
    # the contract this helper exposes is honest.
    return str(result.notes)

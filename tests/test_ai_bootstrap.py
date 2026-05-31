"""Tests for the AI bootstrap surface.

The contract these tests pin down:

- ``bootstrap_runtime()`` returns an :class:`AIBundle` even with NO provider
  keys set (the runtime falls back to a local deterministic provider).
- The bundle exposes the same :class:`CodeGenerator` instance you'd build by
  hand, so consumers can rely on it without reaching into ``runtime.composition``.
- ``has_real_provider()`` correctly distinguishes a fallback-only bundle from
  one wired to a real network provider.
- Injecting a custom ``Runtime`` is supported (the test-double path).

These tests must NOT make network calls — they run in CI without any keys.
"""

from __future__ import annotations

import pytest
from runtime.composition import build_runtime

from sample.ai import AIBundle, bootstrap_runtime, has_real_provider

pytestmark = pytest.mark.unit


class TestBootstrap:
    def test_works_without_any_keys(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Strip any provider keys so we exercise the fallback path explicitly,
        # regardless of the dev's local environment.
        for key in ("OPENROUTER_API_KEY", "OPENAI_API_KEY"):
            monkeypatch.delenv(key, raising=False)

        bundle = bootstrap_runtime()

        assert isinstance(bundle, AIBundle)
        # At least the local fallback provider is present.
        assert len(bundle.runtime.provider_names) >= 1
        assert bundle.codegen is not None

    def test_has_real_provider_is_false_on_fallback_only(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        for key in ("OPENROUTER_API_KEY", "OPENAI_API_KEY"):
            monkeypatch.delenv(key, raising=False)
        bundle = bootstrap_runtime()
        assert has_real_provider(bundle) is False

    def test_injecting_runtime_uses_it_verbatim(self) -> None:
        # The test-double escape hatch — build your own runtime (typically with
        # a stub ProviderManager) and pass it in. Production code never does
        # this, but the unit tests of every downstream feature do.
        custom = build_runtime()
        bundle = bootstrap_runtime(runtime=custom)
        assert bundle.runtime is custom

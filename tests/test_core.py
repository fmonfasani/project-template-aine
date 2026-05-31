"""Smoke test for the demo module. Replace as the real product grows.

The literal ``sample`` package name in the import below is rewritten by
``scripts/init.py`` to the slug you choose at init time.
"""

from __future__ import annotations

import pytest

from sample.core import greet

pytestmark = pytest.mark.unit


class TestGreet:
    def test_uses_the_given_name(self) -> None:
        assert greet("Ada") == "Hello, Ada!"

    @pytest.mark.parametrize("noisy", ["", "   ", "\n\t"])
    def test_falls_back_to_world_on_blank_input(self, noisy: str) -> None:
        # Establishes the project's "be liberal about input" stance on
        # trivial fields -- change as your domain dictates.
        assert greet(noisy) == "Hello, world!"

    def test_trims_surrounding_whitespace(self) -> None:
        assert greet("  Linus  ") == "Hello, Linus!"

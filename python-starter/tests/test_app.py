"""Tests for the core application behavior."""

import pytest

from python_starter import make_greeting


def test_make_greeting() -> None:
    assert make_greeting("Yuva") == "Hello, Yuva!"


def test_make_greeting_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="name must not be empty"):
        make_greeting("   ")

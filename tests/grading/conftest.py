"""Shared fixtures for grading tests.

The ``buggy_query`` fixture monkeypatches ``normalize_query`` back to the
original starter-code behavior, so grading tests can verify that student
properties and test suites are non-trivial (i.e., can actually detect
normalization problems when they exist).
"""

from __future__ import annotations

import re

import pytest

from searchengine import normalize
from searchengine.stopwords import STOPWORDS


def _buggy_normalize_query(text: str) -> list[str]:
    """Replicates the original starter-code behavior of normalize_query."""
    text = text.lower()
    text = text.replace("-", "")
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    return [t for t in tokens if t and t not in STOPWORDS]


@pytest.fixture()
def buggy_query(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch normalize_query back to the original buggy version.

    Patches both the canonical location (searchengine.normalize) and the
    name as imported into the pbt test module, so properties defined with
    ``from searchengine.normalize import normalize_query`` also see the patch.
    """
    import tests.pbt.properties as props_module

    monkeypatch.setattr(normalize, "normalize_query", _buggy_normalize_query)
    monkeypatch.setattr(props_module, "normalize_query", _buggy_normalize_query)

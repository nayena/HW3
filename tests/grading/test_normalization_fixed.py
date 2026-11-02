"""Checks that the normalization bugs are actually fixed.

These tests call normalize_document and normalize_query directly. They do
NOT rely on your test files, so deleting a failing test elsewhere will not
make these pass.
"""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from searchengine.normalize import normalize_document, normalize_query
from tests.pbt.properties import prop_idempotent_document, prop_query_document_consistent


class TestBugsFixed:
    """Task 6: the two bugs in normalize_query."""

    def test_diacritic_bug_fixed(self) -> None:
        """normalize_query should fold diacritics the same way normalize_document does."""
        assert normalize_query("naïve") == normalize_document("naïve"), (
            "normalize_query('naïve') != normalize_document('naïve'), so the "
            "diacritic-folding bug is not fixed"
        )

    def test_hyphen_bug_fixed(self) -> None:
        """normalize_query should handle hyphens the same way normalize_document does."""
        assert normalize_query("co-op") == normalize_document("co-op"), (
            "normalize_query('co-op') != normalize_document('co-op'), so the "
            "hyphen-handling bug is not fixed"
        )

    def test_resume_diacritic_fixed(self) -> None:
        """Diacritic folding applies to other words with diacritics too."""
        assert normalize_query("résumé") == normalize_document("résumé")

    def test_plain_ascii_unaffected(self) -> None:
        """Bug fixes should not break normalization of plain ASCII."""
        assert normalize_query("python") == normalize_document("python")
        assert normalize_query("hello world") == normalize_document("hello world")


# Task 7. These run Hypothesis with a fixed seed (derandomize=True), so they
# try the same inputs every time. On failure they do not print the input they
# found: finding it is the point of Task 7. Your own Hypothesis tests will.


def _holds_for_any_text(prop) -> bool:
    @settings(max_examples=2000, derandomize=True, database=None, deadline=None)
    @given(st.text())
    def check(text: str) -> None:
        assert prop(text)

    try:
        check()
    except AssertionError:
        return False
    return True


class TestHoldsForAnyText:
    """Task 7: the provided properties hold for any string, not just the ones we tried."""

    def test_idempotent_for_any_text(self) -> None:
        if not _holds_for_any_text(prop_idempotent_document):
            pytest.fail(
                "prop_idempotent_document fails for some string. Write a Hypothesis "
                "test for it (Task 7) to find out which.",
                pytrace=False,
            )

    def test_consistent_for_any_text(self) -> None:
        if not _holds_for_any_text(prop_query_document_consistent):
            pytest.fail(
                "prop_query_document_consistent fails for some string. Write a Hypothesis "
                "test for it (Task 7) to find out which.",
                pytrace=False,
            )

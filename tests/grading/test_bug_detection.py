"""Verifies that the student's property functions are non-trivial.

These tests re-introduce the two normalization bugs via the ``buggy_query``
fixture (defined in conftest.py) and assert that the consistency property
returns False for inputs that exercise those bugs.

If a student defines ``prop_query_document_consistent`` to always return True,
or in a way that doesn't actually compare query and document normalization,
these tests will fail.

The ``buggy_query`` fixture is visible to students. Its effect is documented
in conftest.py. Since the bugs are already described in ARTIFACT.md, this is
not a spoiler.
"""

from __future__ import annotations

import pytest

from tests.pbt.properties import prop_query_document_consistent


class TestConsistencyPropertyIsNonTrivial:
    """The consistency property must actually detect the normalization bugs."""

    def test_catches_diacritic_bug(self, buggy_query: pytest.MonkeyPatch) -> None:
        """prop_query_document_consistent should return False for 'naïve' when
        normalize_query has the diacritic-folding bug re-introduced.

        If this test fails, the student's property does not actually compare
        query and document normalization, or always returns True.
        """
        assert not prop_query_document_consistent("naïve"), (
            "prop_query_document_consistent returned True for 'naïve' even with "
            "the diacritic-folding bug active, so the property may be trivially true"
        )

    def test_catches_hyphen_bug(self, buggy_query: pytest.MonkeyPatch) -> None:
        """prop_query_document_consistent should return False for 'co-op' when
        normalize_query has the hyphen-handling bug re-introduced.
        """
        assert not prop_query_document_consistent("co-op"), (
            "prop_query_document_consistent returned True for 'co-op' even with "
            "the hyphen-handling bug active, so the property may be trivially true"
        )

    def test_passes_for_plain_ascii_without_bugs(self) -> None:
        """With bugs fixed, the property should still hold for plain ASCII.

        This is a sanity check: the property should not be trivially False either.
        """
        assert prop_query_document_consistent("hello world"), (
            "prop_query_document_consistent returned False for plain ASCII input "
            "with no bugs active, so the property may be trivially false"
        )

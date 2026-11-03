"""Property-based tests with Hypothesis (Task 7).

Hypothesis is a property-based testing library. It plays the role of your
check_property and your generators: you describe what kind of input you want
(a "strategy", such as st.text() for any string), and Hypothesis generates the
inputs, runs your test on each one, and reports the smallest failing input it
can find.

The test below is a complete example. It reuses a property from properties.py,
the same function your check_property tests call.
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from searchengine.normalize import normalize_document

from .properties import (
    prop_idempotent_document,
    prop_no_empty_tokens_document,
    prop_query_document_consistent,
)


@given(st.text())
def test_no_empty_tokens_any_text(text: str) -> None:
    """No empty tokens, for any string Hypothesis generates."""
    assert prop_no_empty_tokens_document(text)


@settings(max_examples=2000)
@given(st.text())
def test_idempotent_any_text(text: str) -> None:
    """Normalizing a document twice gives the same tokens as normalizing once."""
    assert prop_idempotent_document(text)


@settings(max_examples=2000)
@given(st.text())
def test_query_document_consistent_any_text(text: str) -> None:
    """normalize_query and normalize_document agree on any string."""
    assert prop_query_document_consistent(text)


def test_regression_service_mark_not_idempotent() -> None:
    """Regression: normalize_document was not idempotent for compatibility characters.

    Found by        : Hypothesis, test_idempotent_any_text (st.text(), 2000 examples)
    Hypothesis gave : '℠' (SERVICE MARK)

    The first pass gave ['SM'] and the second gave ['sm']. normalize_document
    lowercased *before* folding diacritics, and the NFKD step of folding
    decomposes '℠' into the two capital letters 'S' 'M'. Those capitals appeared
    after lowercasing had already run, so they survived into the tokens. The
    second pass lowercased them. Fix: fold first, then lowercase.
    """
    assert normalize_document("℠") == ["sm"]
    assert prop_idempotent_document("℠")

"""Provided property definitions for property-based testing.

These properties are predicates: functions that take a single input and
return True if the property holds, or False if it is violated.

DO NOT MODIFY THIS FILE.
Your work goes in test_properties.py. Define new properties there and
add tests for them using check_property.
"""

from __future__ import annotations

from searchengine.normalize import normalize_document, normalize_query


def prop_idempotent_document(text: str) -> bool:
    """normalize_document applied twice should equal applied once.

    If normalization is idempotent, then normalizing already-normalized tokens
    should be a no-op. This is a basic sanity check on the normalizer.
    """
    first = normalize_document(text)
    rejoined = " ".join(first)
    second = normalize_document(rejoined)
    return first == second


def prop_no_empty_tokens_document(text: str) -> bool:
    """normalize_document should never return an empty string as a token."""
    return "" not in normalize_document(text)


def prop_no_empty_tokens_query(text: str) -> bool:
    """normalize_query should never return an empty string as a token."""
    return "" not in normalize_query(text)


def prop_query_document_consistent(text: str) -> bool:
    """normalize_query and normalize_document should agree on any input.

    This property captures the consistency requirement: if the two normalizers
    produce different tokens for the same text, searches will silently fail.

    Note: this property FAILS on the starter code. That is intentional:
    finding this failure is part of the assignment.
    """
    return normalize_query(text) == normalize_document(text)

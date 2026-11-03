"""Property-based tests for the normalization module.

Task 3: Implement check_property in checker.py so these tests can run.
Task 4: Define at least one new prop_ function in this file.
        Add at least one new test class that exercises it (or a provided property)
        with a generator of your choice.
Task 5: Replace the placeholder generators with better ones.
        Add tests that use them and see which ones find failures.
Task 6: When check_property finds a failure, manually minimize the counterexample,
        then add regression test(s) here with the required docstring format.
"""

from __future__ import annotations

import unicodedata

from searchengine.normalize import normalize_query

from .checker import check_property
from .generators import (
    diacritic_word,
    hyphenated_phrase,
    random_printable,
    random_sentence,
    random_word,
)
from .properties import (
    prop_idempotent_document,
    prop_no_empty_tokens_document,
    prop_query_document_consistent,
)

# ---------------------------------------------------------------------------
# Task 4: new properties
# ---------------------------------------------------------------------------


def prop_query_hyphen_is_word_break(text: str) -> bool:
    """In a query, a hyphen separates words exactly like a space does.

    "co-op" must search for the same tokens as "co op". This checks
    normalize_query on its own (not against normalize_document): it fails if
    the query side deletes hyphens and glues the parts together ("coop").
    """
    return normalize_query(text) == normalize_query(text.replace("-", " "))


def prop_query_tokens_have_no_diacritics(text: str) -> bool:
    """Every query token is fully folded: decomposing it reveals no combining marks.

    The index only ever contains folded tokens, so a query token that still
    carries a diacritic (e.g. 'naïve') can never match anything.
    """
    return all(
        unicodedata.category(c) != "Mn"
        for token in normalize_query(text)
        for c in unicodedata.normalize("NFKD", token)
    )


class TestQueryHyphenIsWordBreak:
    def test_hyphen_is_word_break_hyphenated_phrases(self) -> None:
        """A hyphen in a query behaves like a space (hyphenated_phrase generator).

        random_word/random_sentence never produce a hyphen, so they could never
        falsify this property; hyphenated_phrase always does.
        """
        passed, counterexample = check_property(
            prop_query_hyphen_is_word_break,
            hyphenated_phrase,
            trials=300,
            seed=5,
        )
        assert passed, f"Hyphen not treated as a word break for: {counterexample!r}"


class TestQueryTokensFolded:
    def test_query_tokens_folded_diacritic_words(self) -> None:
        """Query tokens contain no diacritics (diacritic_word generator)."""
        passed, counterexample = check_property(
            prop_query_tokens_have_no_diacritics,
            diacritic_word,
            trials=300,
            seed=5,
        )
        assert passed, f"Query token still has a diacritic for: {counterexample!r}"


# ---------------------------------------------------------------------------
# Tests using check_property
# ---------------------------------------------------------------------------


class TestIdempotence:
    def test_idempotent_random_sentences(self) -> None:
        """Idempotence holds for random sentences (naive generator)."""
        passed, counterexample = check_property(
            prop_idempotent_document,
            random_sentence,
            trials=200,
            seed=42,
        )
        assert passed, f"Idempotence violated for: {counterexample!r}"


class TestNoEmptyTokens:
    def test_no_empty_tokens_printable(self) -> None:
        """No empty tokens from random printable strings."""
        passed, counterexample = check_property(
            prop_no_empty_tokens_document,
            random_printable,
            trials=200,
            seed=1,
        )
        assert passed, f"Empty token found for input: {counterexample!r}"

    def test_no_empty_tokens_hyphenated(self) -> None:
        """No empty tokens from hyphenated phrases (e.g. a lone '-' between words)."""
        passed, counterexample = check_property(
            prop_no_empty_tokens_document,
            hyphenated_phrase,
            trials=300,
            seed=1,
        )
        assert passed, f"Empty token found for input: {counterexample!r}"


class TestQueryDocumentConsistency:
    def test_consistency_random_words(self) -> None:
        """Query and document normalization agree on random plain words.

        With the naive generator (lowercase words only), this property likely
        passes, because the naive generator never produces diacritics or hyphens.
        """
        passed, counterexample = check_property(
            prop_query_document_consistent,
            random_word,
            trials=200,
            seed=10,
        )
        assert passed, f"Normalization mismatch for: {counterexample!r}"

    def test_consistency_diacritic_words(self) -> None:
        """Query and document normalization agree on words with diacritics."""
        passed, counterexample = check_property(
            prop_query_document_consistent,
            diacritic_word,
            trials=300,
            seed=7,
        )
        assert passed, f"Normalization mismatch for: {counterexample!r}"

    def test_consistency_hyphenated_phrases(self) -> None:
        """Query and document normalization agree on hyphenated phrases."""
        passed, counterexample = check_property(
            prop_query_document_consistent,
            hyphenated_phrase,
            trials=300,
            seed=7,
        )
        assert passed, f"Normalization mismatch for: {counterexample!r}"




# ---------------------------------------------------------------------------
# Regression tests (Task 6)
# ---------------------------------------------------------------------------
#
# After finding a failure with check_property, add a regression test here.
# A regression test is a plain example-based test for a specific failing input.
#
# Structure:
#
#   def test_regression_<descriptive_name>() -> None:
#       """Regression: <describe what failed and how you found it>."""
#       failing_input = "..."   # the exact counterexample
#       assert prop_<name>(failing_input), f"Regression: {failing_input!r}"
#
# A regression test should be:
# - Named clearly so future readers understand what bug it guards against
# - Accompanied by a docstring explaining how the failure was discovered
# - Standalone (does not call check_property; uses the specific failing input)


def test_regression_diacritic_query_not_folded() -> None:
    """Regression: normalize_query did not fold diacritics; normalize_document did.

    Original counterexample : 'muÏ' (diacritic_word generator, seed=7)
    Minimized counterexample: 'ï'

    Minimization: dropping 'mu' kept the failure ('Ï' alone fails) and lowercasing
    it did too, so a single letter with a diacritic is enough. Removing the Ï
    ('mu') makes it pass: the accent is the whole cause. Document gave ['i'],
    query gave ['ï'].
    """
    assert prop_query_document_consistent("ï"), (
        "ï: document folds the diaeresis to 'i', query must do the same"
    )


def test_regression_hyphen_query_glued() -> None:
    """Regression: normalize_query deleted hyphens instead of splitting on them.

    Original counterexample : 'Ex-dlsbqgbcn;' (hyphenated_phrase generator, seed=7)
    Minimized counterexample: 'x-y'

    Minimization: the trailing ';', the capital letter and the long second part
    were all irrelevant ('ex-d' still fails). Any two non-stopword parts joined by
    one hyphen reproduce it; a hyphen at an edge ('x-', '-y') does not, because
    there is nothing to glue. Document gave ['x', 'y'], query gave ['xy'].
    """
    assert prop_query_document_consistent("x-y"), (
        "x-y: document splits on the hyphen into ['x', 'y'], query must do the same"
    )

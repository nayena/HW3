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

from .checker import check_property
from .generators import (
    random_printable,
    random_sentence,
    random_word,
)
from .properties import (
    prop_idempotent_document,
    prop_no_empty_tokens_document,
    prop_query_document_consistent,
)

# Generators for Tasks 4-5 (import them when you implement them):
# from .generators import diacritic_word, hyphenated_phrase

# ---------------------------------------------------------------------------
# TODO (Task 4): Add at least one new test class below.
# Use check_property with one of the provided properties from .properties
# and a generator of your choice. Which generator is most likely to find
# a failure for each property?
# ---------------------------------------------------------------------------


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

    # TODO (Task 5): After implementing hyphenated_phrase, add a test here
    # that uses it. Does it find a failure the printable generator missed?


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

    # TODO (Task 5): Add a test using diacritic_word as the generator, and one
    # using hyphenated_phrase. Each should find a failure on the starter code.




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

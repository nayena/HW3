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

from hypothesis import given
from hypothesis import strategies as st

from .properties import prop_no_empty_tokens_document


@given(st.text())
def test_no_empty_tokens_any_text(text: str) -> None:
    """No empty tokens, for any string Hypothesis generates."""
    assert prop_no_empty_tokens_document(text)


# TODO (Task 7): Add a Hypothesis test for each of these properties from
# properties.py, using st.text() as the strategy:
#   - prop_idempotent_document
#   - prop_query_document_consistent
# Then follow the rest of Task 7 in ARTIFACT.md.

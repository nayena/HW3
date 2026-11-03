"""Unit tests for the normalization module.

Some tests are provided as working examples.
Your job in Task 2 is to add more, including tests that expose
the normalization bugs lurking in this codebase.
"""

from __future__ import annotations

from searchengine.normalize import fold_diacritics, normalize_document, normalize_query

# ---------------------------------------------------------------------------
# fold_diacritics: provided tests
# ---------------------------------------------------------------------------


class TestFoldDiacritics:
    def test_resume(self) -> None:
        assert fold_diacritics("résumé") == "resume"

    def test_naïve(self) -> None:
        assert fold_diacritics("naïve") == "naive"

    def test_plain_ascii_unchanged(self) -> None:
        assert fold_diacritics("hello") == "hello"

    def test_empty_string(self) -> None:
        assert fold_diacritics("") == ""

    def test_idempotent(self) -> None:
        text = "café naïve résumé"
        assert fold_diacritics(fold_diacritics(text)) == fold_diacritics(text)


# ---------------------------------------------------------------------------
# normalize_document: provided tests
# ---------------------------------------------------------------------------


class TestNormalizeDocument:
    def test_lowercases(self) -> None:
        assert normalize_document("Hello World") == ["hello", "world"]

    def test_strips_punctuation(self) -> None:
        result = normalize_document("hello, world!")
        assert result == ["hello", "world"]

    def test_removes_stopwords(self) -> None:
        result = normalize_document("a quick brown fox")
        assert "a" not in result

    def test_empty_input(self) -> None:
        assert normalize_document("") == []

    def test_all_stopwords(self) -> None:
        assert normalize_document("the a an") == []

    def test_no_empty_tokens(self) -> None:
        result = normalize_document("hello   world")
        assert "" not in result

    def test_diacritics_folded_naive(self) -> None:
        assert normalize_document("naïve") == ["naive"]

    def test_diacritics_folded_resume_uppercase(self) -> None:
        assert normalize_document("RÉSUMÉ") == ["resume"]

    def test_hyphen_splits_into_two_tokens(self) -> None:
        assert normalize_document("co-op") == ["co", "op"]

    def test_hyphen_chain_drops_stopword_parts(self) -> None:
        assert normalize_document("state-of-the-art") == ["state", "art"]

    def test_cpp_loses_plus_signs(self) -> None:
        """'C++' becomes the single letter 'c': the '+' signs are punctuation."""
        assert normalize_document("C++") == ["c"]

    def test_nodejs_dot_removed_not_split(self) -> None:
        """The '.' is stripped, not turned into a space, so it is one token."""
        assert normalize_document("node.js") == ["nodejs"]


# ---------------------------------------------------------------------------
# normalize_query: provided tests
# ---------------------------------------------------------------------------


class TestNormalizeQuery:
    def test_lowercases(self) -> None:
        assert normalize_query("Hello") == ["hello"]

    def test_removes_stopwords(self) -> None:
        result = normalize_query("a search query")
        assert "a" not in result

    def test_empty_input(self) -> None:
        assert normalize_query("") == []

    def test_no_empty_tokens(self) -> None:
        result = normalize_query("hello   world")
        assert "" not in result

    def test_diacritics_folded(self) -> None:
        assert normalize_query("Résumé") == ["resume"]

    def test_hyphen_splits(self) -> None:
        assert normalize_query("well-known") == ["well", "known"]

    def test_strips_punctuation(self) -> None:
        """A query with punctuation searches for the bare words.

        Kills mutant: searchengine.normalize.x_normalize_query__mutmut_19
        """
        assert normalize_query("Node.js, please!") == ["nodejs", "please"]


# ---------------------------------------------------------------------------
# Consistency tests: provided (some of these FAIL because they expose the bugs)
# ---------------------------------------------------------------------------


class TestNormalizationConsistency:
    """Query and document normalization should agree.

    If they disagree, a user who searches for a term will not find
    documents that contain that term. The search fails silently.

    Two of these tests fail on the starter code.
    """

    def test_plain_ascii_consistent(self) -> None:
        """Basic ASCII text normalizes the same way for docs and queries."""
        assert normalize_query("hello world") == normalize_document("hello world")

    def test_diacritic_consistency(self) -> None:
        """'naïve' should normalize the same way whether in a doc or a query.

        This test FAILS on the starter code.
        """
        assert normalize_query("naïve") == normalize_document("naïve")

    def test_hyphen_consistency(self) -> None:
        """'co-op' should normalize the same way whether in a doc or a query.

        This test FAILS on the starter code.
        """
        assert normalize_query("co-op") == normalize_document("co-op")

    def test_resume_consistency(self) -> None:
        assert normalize_query("résumé") == normalize_document("résumé")

    def test_multi_hyphen_consistency(self) -> None:
        assert normalize_query("state-of-the-art") == normalize_document("state-of-the-art")

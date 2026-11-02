"""Integration tests for the full search pipeline.

Tests here exercise document loading, indexing, and retrieval together.
Some tests are provided; add more in Task 2.

Two integration tests fail on the starter code (same underlying bugs as
test_normalize.py's consistency tests).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from searchengine.corpus import load_corpus
from searchengine.search import SearchEngine

CORPUS_DIR = Path(__file__).parent.parent / "corpus" / "docs"


@pytest.fixture(scope="module")
def engine() -> SearchEngine:
    """Build a SearchEngine over the real corpus. Shared across tests."""
    docs = load_corpus(CORPUS_DIR)
    return SearchEngine(docs)


# ---------------------------------------------------------------------------
# Provided tests: these pass on the starter code
# ---------------------------------------------------------------------------


class TestBasicSearch:
    def test_returns_results_for_known_term(self, engine: SearchEngine) -> None:
        results = engine.search("python")
        assert len(results) > 0

    def test_returns_empty_for_unknown_term(self, engine: SearchEngine) -> None:
        results = engine.search("xyzzy")
        assert results == []

    def test_result_has_expected_fields(self, engine: SearchEngine) -> None:
        results = engine.search("python")
        for r in results:
            assert r.doc_id
            assert r.title
            assert isinstance(r.snippet, str)

    def test_stopword_only_query_returns_nothing(self, engine: SearchEngine) -> None:
        results = engine.search("the a an")
        assert results == []

    def test_multi_word_query_uses_and_semantics(self, engine: SearchEngine) -> None:
        # Both "python" and "language" should appear in at least one document.
        results = engine.search("python language")
        for r in results:
            # The result should be a document containing both terms.
            assert r.doc_id


# ---------------------------------------------------------------------------
# Provided tests: these FAIL on the starter code
# ---------------------------------------------------------------------------


class TestEdgeCaseSearch:
    """Integration tests for edge-case queries.

    Some of these tests fail on the starter code.
    """

    def test_diacritic_query_finds_document(self, engine: SearchEngine) -> None:
        """Searching 'naïve' should find the document about naïve ML.

        This FAILS on the starter code.
        """
        results = engine.search("naïve")
        doc_ids = [r.doc_id for r in results]
        assert "naive_ml" in doc_ids

    def test_hyphenated_query_finds_document(self, engine: SearchEngine) -> None:
        """Searching 'co-op' should find the document about co-op programs.

        This FAILS on the starter code.
        """
        results = engine.search("co-op")
        doc_ids = [r.doc_id for r in results]
        assert "coop_programs" in doc_ids

    # TODO (Task 2): Add at least two more integration tests.
    # Ideas:
    # - "résumé" should find the resume tips document
    # - A multi-word query that should return a specific known document
    # - Verify that fixing the bugs does not break other queries

"""Search engine: query processing and result retrieval."""

from __future__ import annotations

from dataclasses import dataclass

from searchengine.corpus import Document
from searchengine.index import InvertedIndex
from searchengine.normalize import normalize_query


@dataclass
class SearchResult:
    """A single search result."""

    doc_id: str
    title: str
    score: float
    snippet: str


class SearchEngine:
    """A simple AND-semantics search engine over a document corpus.

    Documents are indexed at construction time using normalize_document.
    Queries are processed using normalize_query. If these two normalizers
    disagree, searches can silently fail to return relevant results.
    """

    def __init__(self, documents: list[Document]) -> None:
        self._documents: dict[str, Document] = {
            doc.doc_id: doc for doc in documents
        }
        self._index = InvertedIndex()
        for doc in documents:
            self._index.add_document(doc.doc_id, doc.content)

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        """Search for documents matching all tokens in the query.

        Uses AND semantics: every query token must appear in the document.
        Results are returned sorted by doc_id (deterministic ordering).
        Returns at most top_k results.
        """
        tokens = normalize_query(query)
        if not tokens:
            return []

        candidate_sets = [set(self._index.search(t)) for t in tokens]
        matching = candidate_sets[0]
        for s in candidate_sets[1:]:
            matching = matching & s

        results = []
        for doc_id in sorted(matching):
            doc = self._documents[doc_id]
            results.append(
                SearchResult(
                    doc_id=doc_id,
                    title=doc.title,
                    score=1.0,
                    snippet=self._make_snippet(doc.content),
                )
            )

        return results[:top_k]

    def _make_snippet(self, content: str, max_chars: int = 120) -> str:
        """Return a short preview of the document body (skipping the title line)."""
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        body = " ".join(lines[1:]) if len(lines) > 1 else " ".join(lines)
        if len(body) > max_chars:
            body = body[:max_chars].rsplit(" ", 1)[0] + "..."
        return body

"""Inverted index mapping tokens to document IDs."""

from __future__ import annotations

from collections import defaultdict

from searchengine.normalize import normalize_document


class InvertedIndex:
    """A simple inverted index.

    Maps each normalized token to the list of document IDs that contain it.
    Documents are indexed using normalize_document.
    """

    def __init__(self) -> None:
        self._index: dict[str, list[str]] = defaultdict(list)
        self._doc_count: int = 0

    def add_document(self, doc_id: str, text: str) -> None:
        """Index a document by extracting and storing its tokens."""
        tokens = normalize_document(text)
        seen: set[str] = set()
        for token in tokens:
            if token not in seen:
                self._index[token].append(doc_id)
                seen.add(token)
        self._doc_count += 1

    def search(self, token: str) -> list[str]:
        """Return all document IDs that contain the given (already-normalized) token."""
        return list(self._index.get(token, []))

    def vocabulary(self) -> set[str]:
        """Return all tokens currently in the index."""
        return set(self._index.keys())

    def __len__(self) -> int:
        return self._doc_count

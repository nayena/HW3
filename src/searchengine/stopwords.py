"""Stopwords for the search engine.

Words in this set are stripped from both documents and queries during
normalization. Removing common words reduces noise but can cause
surprising failures. For example, try searching for "The Who".

Defined here (not in normalize.py) so that mutation testing stays
focused on normalization logic rather than individual stopword entries.
"""

from __future__ import annotations

STOPWORDS: frozenset[str] = frozenset({
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "of", "in", "on", "at",
    "to", "for", "with", "by", "from", "and", "or", "but", "not", "it",
    "its", "this", "that", "these", "those", "as", "if", "so", "yet",
})

"""Text normalization for the search engine.

This module processes raw text into tokens for indexing and searching.
All documents and queries pass through normalization before being indexed
or searched.

Two public functions:
    normalize_document(text) -> list of index tokens
    normalize_query(text)    -> list of search tokens

These should behave consistently. If they disagree, searches may silently
fail to return relevant results.
"""

from __future__ import annotations

import re
import unicodedata

from searchengine.stopwords import STOPWORDS


def fold_diacritics(text: str) -> str:
    """Convert letters with diacritics to their ASCII equivalents.

    Uses NFKD normalization to decompose characters, then strips combining
    (diacritic) code points.

    Examples:
        "résumé"   -> "resume"
        "naïve"    -> "naive"
        "Ångström" -> "Angstrom"
        "hello"    -> "hello"
    """
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def normalize_document(text: str) -> list[str]:
    """Normalize a document string and return a list of index tokens.

    Steps:
        1. Lowercase
        2. Fold diacritics  (naïve -> naive, résumé -> resume)
        3. Replace hyphens with spaces  (co-op -> "co op")
        4. Strip remaining punctuation
        5. Split on whitespace
        6. Filter empty strings and stopwords
    """
    text = text.lower()
    text = fold_diacritics(text)
    text = text.replace("-", " ")
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    return [t for t in tokens if t and t not in STOPWORDS]


def normalize_query(text: str) -> list[str]:
    """Normalize a query string and return a list of search tokens.

    Steps:
        1. Lowercase
        2. Handle hyphens
        3. Strip remaining punctuation
        4. Split on whitespace
        5. Filter empty strings and stopwords
    """
    text = text.lower()
    text = text.replace("-", "")
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    return [t for t in tokens if t and t not in STOPWORDS]

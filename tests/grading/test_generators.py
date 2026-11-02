"""Meta-tests: checks that the Task 5 generators produce varied, useful inputs.

These tests are visible to students and run as part of `make grade` and CI.
They check the shape of what your generators produce, not whether they find
bugs. A generator can pass all of them and still miss a bug, so also look at
what your property tests report when they use it.
"""

from __future__ import annotations

import random
import unicodedata

from tests.pbt.generators import diacritic_word, hyphenated_phrase

SAMPLE_SIZE = 200
SEED = 42


def _sample(generator, n: int = SAMPLE_SIZE) -> list[str]:
    rng = random.Random(SEED)
    return [generator(rng) for _ in range(n)]


def _diacritic_marks(text: str) -> set[str]:
    """The combining diacritical marks in `text`, by Unicode name (e.g. 'COMBINING ACUTE ACCENT')."""
    decomposed = unicodedata.normalize("NFD", text)
    return {unicodedata.name(c) for c in decomposed if unicodedata.category(c) == "Mn"}


class TestDiacriticWord:
    def test_mostly_non_ascii(self) -> None:
        """Most generated words should contain at least one non-ASCII character."""
        samples = _sample(diacritic_word)
        non_ascii = [s for s in samples if not s.isascii()]
        assert len(non_ascii) >= SAMPLE_SIZE // 2, (
            f"diacritic_word produced {len(non_ascii)}/{SAMPLE_SIZE} words with a non-ASCII "
            "character. Is it still the placeholder?"
        )

    def test_non_ascii_chars_are_letters(self) -> None:
        """Non-ASCII characters should be letters with diacritics, not arbitrary Unicode."""
        for word in _sample(diacritic_word):
            for ch in word:
                if not ch.isascii():
                    category = unicodedata.category(ch)
                    assert category.startswith("L"), (
                        f"diacritic_word produced {word!r}, which contains {ch!r} "
                        f"(Unicode category {category}, not a letter)"
                    )

    def test_several_kinds_of_diacritic(self) -> None:
        """Words should use several kinds of diacritical mark, not just one or two."""
        marks: set[str] = set()
        for word in _sample(diacritic_word):
            marks |= _diacritic_marks(word)
        assert len(marks) >= 4, (
            f"diacritic_word used {len(marks)} kind(s) of diacritical mark in {SAMPLE_SIZE} words: "
            f"{sorted(marks)}. Real text uses more kinds than that."
        )

    def test_many_distinct_words(self) -> None:
        """A generator should explore beyond a short list of words you thought of."""
        distinct = set(_sample(diacritic_word))
        assert len(distinct) >= SAMPLE_SIZE // 4, (
            f"diacritic_word produced {len(distinct)} distinct words in {SAMPLE_SIZE} calls. "
            "A generator that only repeats a short list can only test inputs you "
            "already thought of."
        )


class TestHyphenatedPhrase:
    def test_mostly_hyphenated(self) -> None:
        """Most generated phrases should contain a hyphen."""
        samples = _sample(hyphenated_phrase)
        hyphenated = [s for s in samples if "-" in s]
        assert len(hyphenated) >= SAMPLE_SIZE // 2, (
            f"hyphenated_phrase produced {len(hyphenated)}/{SAMPLE_SIZE} strings with a "
            "hyphen. Is it still the placeholder?"
        )

    def test_hyphen_connects_word_parts(self) -> None:
        """Hyphens should appear between word parts, not at the edges."""
        for phrase in _sample(hyphenated_phrase):
            assert not phrase.startswith("-"), f"phrase starts with a hyphen: {phrase!r}"
            assert not phrase.endswith("-"), f"phrase ends with a hyphen: {phrase!r}"

    def test_some_phrases_have_several_hyphens(self) -> None:
        """Compound words can have more than one hyphen (state-of-the-art)."""
        samples = _sample(hyphenated_phrase)
        several = [s for s in samples if s.count("-") >= 2]
        assert len(several) >= SAMPLE_SIZE // 10, (
            f"hyphenated_phrase produced {len(several)}/{SAMPLE_SIZE} phrases with two or "
            "more hyphens."
        )

    def test_many_distinct_phrases(self) -> None:
        """A generator should explore beyond a short list of phrases you thought of."""
        distinct = set(_sample(hyphenated_phrase))
        assert len(distinct) >= SAMPLE_SIZE // 4, (
            f"hyphenated_phrase produced {len(distinct)} distinct phrases in {SAMPLE_SIZE} "
            "calls. A generator that only repeats a short list can only test inputs you "
            "already thought of."
        )

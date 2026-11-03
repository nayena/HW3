"""Input generators for property-based testing.

Each generator is a function:  rng: random.Random -> value

Using the RNG object (not the global random module) keeps generation
deterministic when a seed is supplied to check_property.

Tasks 4-5: Use these generators in test_properties.py.
Task 5: Replace the two placeholder generators with real ones.
"""

from __future__ import annotations

import random
import string
import unicodedata

from searchengine.stopwords import STOPWORDS

# ---------------------------------------------------------------------------
# Provided generators: naive but functional
# ---------------------------------------------------------------------------


def random_word(rng: random.Random) -> str:
    """A random lowercase alphabetic word (1-12 characters)."""
    length = rng.randint(1, 12)
    return "".join(rng.choice(string.ascii_lowercase) for _ in range(length))


def random_sentence(rng: random.Random) -> str:
    """A random sequence of 1-10 lowercase words separated by spaces."""
    n = rng.randint(1, 10)
    return " ".join(random_word(rng) for _ in range(n))


def random_printable(rng: random.Random) -> str:
    """A random string of printable ASCII characters (0-30 characters)."""
    length = rng.randint(0, 30)
    return "".join(rng.choice(string.printable) for _ in range(length))


# ---------------------------------------------------------------------------
# Domain-aware generators (Task 5)
# ---------------------------------------------------------------------------


def _build_accented_letters() -> list[str]:
    """Every single precomposed letter that is an ASCII letter plus one or two marks.

    Built from Unicode itself (not a hand-written list), so it covers lowercase
    and uppercase letters and many kinds of mark: acute, grave, circumflex,
    diaeresis, tilde, cedilla, ring, caron, macron, breve, ogonek, dot above,
    dot below, double acute, hook, horn, and stacked combinations such as ǖ or ệ.
    """
    marks = [chr(c) for c in range(0x0300, 0x0370)] + ["᷀", "᷁"]
    found: set[str] = set()
    for base in string.ascii_letters:
        for m1 in marks:
            one = unicodedata.normalize("NFC", base + m1)
            if len(one) == 1 and unicodedata.category(one).startswith("L"):
                found.add(one)
                for m2 in marks:
                    two = unicodedata.normalize("NFC", one + m2)
                    if len(two) == 1 and unicodedata.category(two).startswith("L"):
                        found.add(two)
    return sorted(found)


_ACCENTED = _build_accented_letters()

# Common accented letters from real text, weighted more heavily than the long tail.
_COMMON_ACCENTED = list("éèêëàâäáãåîïíìôöóòõøùûüúçñÉÈÊËÀÂÄÁÃÅÎÏÍÔÖÓÙÛÜÚÇÑ")

# Letters that fold through *compatibility* decomposition (NFKD), not just NFD:
# ligatures, long s, and similar. A normalizer using NFD/NFC instead of NFKD
# treats these differently.
_COMPAT_LETTERS = list("ﬁﬂﬀﬃﬄſǆǅǄĳĲ")

_REAL_WORDS = [
    "résumé", "naïve", "café", "façade", "jalapeño", "piñata", "crème", "brûlée",
    "über", "Zürich", "São", "Paulo", "coöperate", "Ångström", "señor", "Noël",
    "fiancée", "déjà", "vu", "El", "Niño", "Mötley", "Crüe", "naïveté", "Bogotá",
]


def _accent(rng: random.Random) -> str:
    roll = rng.random()
    if roll < 0.5:
        return rng.choice(_COMMON_ACCENTED)
    if roll < 0.9:
        return rng.choice(_ACCENTED)
    return rng.choice(_COMPAT_LETTERS)


def _decorate_with_accents(rng: random.Random, word: str) -> str:
    """Replace one or more letters in `word` with accented letters (at least one)."""
    chars = list(word)
    n = rng.randint(1, max(1, len(chars) // 2))
    for i in rng.sample(range(len(chars)), min(n, len(chars))):
        chars[i] = _accent(rng)
    return "".join(chars)


def _apply_case(rng: random.Random, word: str) -> str:
    roll = rng.random()
    if roll < 0.6:
        return word
    if roll < 0.8:
        return word.capitalize()
    if roll < 0.9:
        return word.upper()
    return "".join(c.upper() if rng.random() < 0.5 else c for c in word)


def diacritic_word(rng: random.Random) -> str:
    """A word containing at least one letter with a diacritic.

    Mixes several strategies so the output varies in many directions:
      - a random ASCII word with some letters replaced by accented letters,
        drawn from common ones (é, ï, ñ, ç, ...) and from every precomposed
        Latin letter + mark(s) Unicode has (ǖ, ệ, ő, ț, ...);
      - a real word that has diacritics (résumé, naïve, ...), sometimes with
        extra accents added;
      - compatibility letters (ligatures like ﬁ, long s ſ) that only NFKD folds;
      - random capitalization (É vs é), since case and folding interact.
    """
    if rng.random() < 0.25:
        word = rng.choice(_REAL_WORDS)
        if rng.random() < 0.5:
            word = _decorate_with_accents(rng, word)
    else:
        word = _decorate_with_accents(rng, random_word(rng))
    return _apply_case(rng, word)


def _hyphen_part(rng: random.Random) -> str:
    """One piece of a hyphenated compound. Not just plain words."""
    roll = rng.random()
    if roll < 0.40:
        part = random_word(rng)
    elif roll < 0.55:
        part = rng.choice(sorted(STOPWORDS))           # state-OF-THE-art
    elif roll < 0.65:
        part = str(rng.randint(0, 2025))                # covid-19, 2-3
    elif roll < 0.72:
        part = rng.choice(string.ascii_letters)         # x-ray, e-mail
    elif roll < 0.85:
        part = diacritic_word(rng)                      # café-crème
    elif roll < 0.92:
        part = random_word(rng) + str(rng.randint(0, 99))  # mp3-player
    else:
        part = rng.choice(["co", "re", "pre", "non", "self", "anti", "ex", "well"])
    return _apply_case(rng, part)


def hyphenated_phrase(rng: random.Random) -> str:
    """A hyphenated compound, sometimes inside a short phrase.

    Variation in every direction that matters for hyphen handling:
      - 2 to 5 parts, so some phrases have several hyphens (state-of-the-art);
      - parts that are words, stopwords, numbers, single letters, words with
        diacritics, or prefixes (co-, re-, self-);
      - mostly single hyphens, occasionally doubled (word--word);
      - sometimes surrounded by other words.
    """
    n_parts = rng.choice([2, 2, 2, 3, 3, 4, 5])
    parts = [_hyphen_part(rng) for _ in range(n_parts)]
    seps = ["--" if rng.random() < 0.08 else "-" for _ in range(n_parts - 1)]
    compound = parts[0] + "".join(s + p for s, p in zip(seps, parts[1:], strict=True))

    if rng.random() < 0.3:
        before = [random_word(rng) for _ in range(rng.randint(0, 2))]
        after = [random_word(rng) for _ in range(rng.randint(0, 2))]
        compound = " ".join([*before, compound, *after])
    return compound


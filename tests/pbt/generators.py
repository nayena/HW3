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


def diacritic_word(rng: random.Random) -> str:
    """A word that may contain letters with diacritics.

    TODO (Task 5): Implement this generator.

    Hint: consider characters like é, è, ê, ë, à, â, î, ï, ô, ù, û, ü, ç, ñ.
    One approach: take a plain word and randomly replace some characters with
    variants that carry diacritics. Another: draw from a list of real words
    that contain them (résumé, naïve, café, façade, jalapeño, …).

    The goal is to generate inputs that will stress the diacritic-folding
    behavior of the normalizer.
    """
    # Placeholder: returns a plain word. Replace with a real implementation.
    return random_word(rng)


def hyphenated_phrase(rng: random.Random) -> str:
    """A hyphenated compound word or phrase.

    TODO (Task 5): Implement this generator.

    Examples: co-op, well-known, twenty-three, self-aware, state-of-the-art,
    first-class, user-defined, real-time.

    The goal is to generate inputs that stress hyphen-handling in the normalizer.
    """
    # Placeholder: returns a plain word. Replace with a real implementation.
    return random_word(rng)


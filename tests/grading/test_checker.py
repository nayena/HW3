"""Meta-tests: verifies that check_property is correctly implemented.

These tests are visible to students and run as part of normal CI.
They serve two purposes:
  - Give students immediate feedback if their check_property implementation
    has a correctness bug (rather than failing silently in test_properties.py).
  - Give the instructor an automated signal that Task 3 is complete.
"""

from __future__ import annotations

from tests.pbt.checker import check_property


# ---------------------------------------------------------------------------
# Helpers (simple, self-contained, no dependency on searchengine)
# ---------------------------------------------------------------------------


def _gen_int(rng):
    return rng.randint(0, 100)


def _gen_string(rng):
    return "".join(rng.choice("abcde") for _ in range(rng.randint(0, 10)))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestCheckPropertyBasics:
    def test_returns_true_when_property_always_holds(self) -> None:
        """All inputs satisfy the property → (True, None)."""
        passed, ce = check_property(lambda x: True, _gen_int, trials=100, seed=0)
        assert passed is True
        assert ce is None

    def test_returns_false_when_property_never_holds(self) -> None:
        """No inputs satisfy the property → (False, counterexample)."""
        passed, ce = check_property(lambda x: False, _gen_int, trials=10, seed=0)
        assert passed is False
        assert ce is not None

    def test_counterexample_satisfies_negation(self) -> None:
        """The returned counterexample actually violates the property."""
        passed, ce = check_property(lambda n: n < 50, _gen_int, trials=200, seed=1)
        if not passed:
            assert ce >= 50

    def test_exception_in_property_counts_as_failure(self) -> None:
        """If prop raises, that input is treated as a counterexample."""
        def prop_raises(x):
            raise ValueError("deliberate")

        passed, ce = check_property(prop_raises, _gen_int, trials=1, seed=0)
        assert passed is False
        assert ce is not None

    def test_seed_produces_reproducible_results(self) -> None:
        """Same seed → same counterexample every time."""
        prop = lambda n: n < 50  # noqa: E731

        _, ce1 = check_property(prop, _gen_int, trials=200, seed=42)
        _, ce2 = check_property(prop, _gen_int, trials=200, seed=42)
        assert ce1 == ce2

    def test_different_seeds_may_differ(self) -> None:
        """Different seeds should generally produce different sequences.

        This is a probabilistic test: it checks that seeding has any effect
        at all. It could theoretically pass even with identical sequences,
        but in practice will not.
        """
        results = set()
        for s in range(10):
            _, ce = check_property(lambda n: n < 50, _gen_int, trials=200, seed=s)
            if ce is not None:
                results.add(ce)
        # With 10 different seeds, we expect at least 2 distinct counterexamples.
        assert len(results) >= 2

    def test_no_seed_still_runs(self) -> None:
        """check_property runs without a seed (non-reproducible is fine)."""
        passed, _ = check_property(lambda x: True, _gen_int, trials=20, seed=None)
        assert passed is True

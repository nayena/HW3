"""A minimal property-based testing mechanism.

Your job in Task 3 is to implement `check_property`.

The goal is not to replicate Hypothesis or any existing PBT library.
The goal is to understand the core idea by building a small version yourself.

A correct implementation is a simple loop: generate inputs, check the property,
report the first failure.
"""

from __future__ import annotations

import random
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")

# Type aliases for readability.
Property = Callable[[T], bool]        # input -> True (pass) or False (fail)
Generator = Callable[[random.Random], T]  # rng -> generated input


def check_property(
    prop: Property,
    generator: Generator,
    trials: int = 100,
    seed: int | None = None,
) -> tuple[bool, Any]:
    """Run `trials` random trials, checking that `prop` holds for each input.

    Parameters
    ----------
    prop:
        A function that takes a generated input and returns True if the
        property holds, or False if it is violated.
    generator:
        A function that takes a `random.Random` instance and returns a
        generated input. Use the provided RNG (not the global `random`
        module) so that results are reproducible when a seed is given.
    trials:
        Number of random inputs to generate and test. Default: 100.
    seed:
        Optional integer seed for the RNG. When provided, the same sequence
        of inputs is produced every time, which is essential for reproducible failures
        and regression tests.

    Returns
    -------
    (True, None)
        if all `trials` inputs satisfy `prop`.
    (False, counterexample)
        where `counterexample` is the first input for which `prop` returned
        False or raised an exception.

    Notes
    -----
    - If `prop` raises an exception on some input, treat that as a failure.
      The counterexample should be the input that caused the exception.
    - The `seed` parameter matters: a fixed seed lets you turn a discovered
      failure into a reproducible regression test.
    - You do not need to implement shrinking (counterexample minimization).
      If you find a failure, report it as-is.

    Example
    -------
    >>> def prop_short(s):
    ...     return len(s) < 10
    >>> def gen_string(rng):
    ...     return ''.join(rng.choice('abc') for _ in range(rng.randint(0, 15)))
    >>> passed, ce = check_property(prop_short, gen_string, trials=50, seed=42)
    """
    # TODO (Task 3): Implement this function.
    #
    # Steps:
    #   1. Create a random.Random instance.
    #      If `seed` is not None, call rng.seed(seed) on it.
    #   2. Loop `trials` times:
    #      a. Generate an input:  inp = generator(rng)
    #      b. Try calling prop(inp).
    #         - If it returns False → return (False, inp)
    #         - If it raises any exception → return (False, inp)
    #   3. If all trials pass → return (True, None)
    raise NotImplementedError(
        "Implement check_property in tests/pbt/checker.py (Task 3)"
    )

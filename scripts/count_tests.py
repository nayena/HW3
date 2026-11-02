"""Count collected tests across student-written test files.

Used by CI to enforce the minimum new-test requirement.
Prints the integer count to stdout.

Uses pytest's Python API rather than parsing text output,
so it is not sensitive to pytest version or output format changes.
"""
import pytest


class _Counter:
    count = 0

    def pytest_collection_finish(self, session: pytest.Session) -> None:
        self.count = len(session.items)


counter = _Counter()
pytest.main(
    [
        "tests/test_normalize.py",
        "tests/test_search.py",
        "tests/pbt/test_properties.py",
        "tests/pbt/test_hypothesis.py",
        "--collect-only",
        "-q",
        "-p",
        "no:cacheprovider",
    ],
    plugins=[counter],
)
print(counter.count)

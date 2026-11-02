"""Check the mutants your tests claim to kill (Task 8).

Finds every test whose docstring contains a line like

    Kills mutant: searchengine.search.xǁSearchEngineǁsearch__mutmut_12

and runs mutmut on that one mutant twice, in a scratch copy of the repo:
once with your test suite, and once with that test left out. The claim
holds if the mutant is killed the first time and survives the second.

Like `make mutmut`, it leaves out your Hypothesis tests (every @given test),
so the kill has to come from an example-based or check_property test.

Run it with `make kills`. Exits non-zero if any claim does not hold, or if
no test makes a claim.
"""

from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST_FILES = ["tests/test_normalize.py", "tests/test_search.py", "tests/pbt"]
MARKER = re.compile(r"^\s*Kills mutant:\s*(\S+)\s*$", re.MULTILINE)
SKIP = shutil.ignore_patterns(
    ".git", "mutants", ".mutmut-cache", ".pytest_cache", ".ruff_cache", ".hypothesis",
    "__pycache__", ".venv",
)


def find_claims() -> list[tuple[str, str]]:
    """Return (pytest node id, mutant name) for each claim in the test files."""
    paths: list[Path] = []
    for entry in TEST_FILES:
        p = ROOT / entry
        paths += sorted(p.glob("test_*.py")) if p.is_dir() else [p]

    claims = []
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT).as_posix()
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                funcs = [(f"{rel}::{node.name}", f) for f in node.body]
            else:
                funcs = [(rel, node)]
            for prefix, func in funcs:
                if not isinstance(func, ast.FunctionDef) or not func.name.startswith("test"):
                    continue
                for name in MARKER.findall(ast.get_docstring(func) or ""):
                    claims.append((f"{prefix}::{func.name}", name))
    return claims


def mutant_status(mutant: str, deselect: str | None) -> str:
    """Run mutmut on one mutant in a scratch copy; return its status (e.g. 'killed')."""
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "repo"
        shutil.copytree(ROOT, work, ignore=SKIP)
        if deselect:
            pyproject = work / "pyproject.toml"
            text = pyproject.read_text(encoding="utf-8")
            extra = f'[tool.mutmut]\npytest_add_cli_args = ["--deselect", "{deselect}"]\n'
            pyproject.write_text(text.replace("[tool.mutmut]\n", extra, 1), encoding="utf-8")
        env = {**os.environ, "PYTEST_ADDOPTS": '-m "not hypothesis"'}
        run = subprocess.run(
            ["mutmut", "run", mutant], cwd=work, env=env,
            capture_output=True, text=True, check=False,
        )
        if "failed to collect stats" in run.stdout + run.stderr:
            return "suite fails"
        results = subprocess.run(
            ["mutmut", "results", "--all", "true"],
            cwd=work, capture_output=True, text=True, check=False,
        ).stdout
    for line in results.splitlines():
        name, _, status = line.strip().rpartition(": ")
        if name == mutant:
            return status
    return "not found"


def main() -> int:
    claims = find_claims()
    if not claims:
        print("No test has a 'Kills mutant: <name>' line in its docstring yet (Task 8).")
        return 1

    ok = True
    for test, mutant in claims:
        print(f"{test}\n  claims to kill {mutant}")
        with_test = mutant_status(mutant, deselect=None)
        if with_test == "suite fails":
            print("  NO: your tests fail on the unmutated code, so mutmut cannot run. Try `make test`.")
            return 1
        if with_test == "not found":
            print("  NO: mutmut has no mutant with that name. Copy the name from `make results`.")
            ok = False
            continue
        without_test = mutant_status(mutant, deselect=test)
        print(f"  with this test: {with_test}; without it: {without_test}")
        if with_test == "killed" and without_test == "survived":
            print("  OK")
        elif with_test != "killed":
            print("  NO: the mutant is not killed even with this test.")
            ok = False
        else:
            print("  NO: the mutant is killed even without this test, so another test kills it.")
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

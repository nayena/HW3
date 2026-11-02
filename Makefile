# HW3 Makefile - Search Engine Testing
#
# Every target is a short command you could also type yourself. Run `make help`
# to list them. The tools (pytest, ruff, mutmut) are already installed in the
# dev container, so there is nothing to set up first.

.PHONY: help test lint grade check mutmut mutmut-all results kills clean

# Let Python find the searchengine package in src/
export PYTHONPATH := $(CURDIR)/src

help:
	@echo "make test        run the test suite (tests/test_*.py and tests/pbt/)"
	@echo "make lint        run the linter on src/"
	@echo "make grade       run the grading checks in tests/grading/"
	@echo "make check       lint + test + grade, the same checks CI runs"
	@echo "make mutmut      mutation testing without your Hypothesis tests (Task 8)"
	@echo "make mutmut-all  mutation testing with all your tests (Task 8)"
	@echo "make results     list the mutants that survived the last mutmut run"
	@echo "make kills       check the mutants your tests claim to kill (Task 8)"
	@echo "make clean       remove caches and mutmut's working files"

test:
	pytest

lint:
	ruff check src/

grade:
	pytest tests/grading/

check: lint test grade

# Task 8 runs mutmut twice. `make mutmut` leaves out your Hypothesis tests
# (pytest's `-m "not hypothesis"` skips every @given test); `make mutmut-all`
# runs all of them. mutmut doesn't notice which tests were left out, so each
# run deletes mutants/ and starts over. `mutmut run` exits with an error when
# any mutant survives, which is normal here, so the `-` tells make to keep going.
mutmut:
	rm -rf mutants/
	-PYTEST_ADDOPTS='-m "not hypothesis"' mutmut run
	mutmut results --all true > mutmut_results.txt
	@echo "Saved mutmut_results.txt (without your Hypothesis tests). Commit it with your submission."

mutmut-all:
	rm -rf mutants/
	-mutmut run
	mutmut results --all true > mutmut_results_all.txt
	@echo "Saved mutmut_results_all.txt (all your tests). Commit it with your submission."

results:
	mutmut results

kills:
	python scripts/check_kills.py

clean:
	rm -rf mutants/ .mutmut-cache .pytest_cache .ruff_cache .hypothesis
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

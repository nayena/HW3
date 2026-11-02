# Artifact Instructions

This document describes the technical work required for HW3. Do the tasks in order: each one builds on the ones before it.

---

## Current State: Tests Are Failing

When you open this repository, **seven tests fail**. This is intentional.

Run them to see:

```bash
make test
```

- Two tests in `test_normalize.py` (`test_diacritic_consistency`, `test_hyphen_consistency`) and two in `test_search.py` (`test_diacritic_query_finds_document`, `test_hyphenated_query_finds_document`) fail because of bugs in the search engine. You'll find and fix them in Task 6.
- Three tests in `tests/pbt/test_properties.py` fail with `NotImplementedError` until you write `check_property` in Task 3.

Lint passes on the starter code (`make lint`). Keep it that way.

`make grade` runs the grading checks in `tests/grading/`. Most of them fail at the start, and each task makes some of them pass. They are visible so you can check your own work, and the autograder runs the same checks.

---

## Understanding the System

Before writing any tests, read the code in this order:

1. `corpus/docs/`: what documents exist; notice which ones have diacritics (é, ï, ñ, ...), hyphens, and punctuation
2. `src/searchengine/corpus.py`: how documents are loaded
3. `src/searchengine/normalize.py`: **the center of this assignment**; read it carefully
4. `src/searchengine/index.py`: how words are stored in the inverted index
5. `src/searchengine/search.py`: how queries are answered
6. `src/searchengine/cli.py`: the `search` command

Then try the search engine in the container terminal:

```bash
search list-docs
search search "python"
search search "naïve"
search explain "co-op"
search explain "naïve"
```

The `explain` command is especially useful: it shows how a string is normalized as part of a document and as part of a query, side by side. What do you notice?

---

## Tasks

---

### Task 1: Orient Yourself

No code to write. Before starting Task 2, make sure you can answer these questions by reading the source and trying the commands above:

- Where are documents loaded? Where does normalization happen for documents? For queries?
- What does `normalize_document("naïve")` return? What does `normalize_query("naïve")` return?
- What does `normalize_document("co-op")` return? What does `normalize_query("co-op")` return?
- Why does `test_diacritic_consistency` fail? Why does `test_hyphen_consistency` fail?

You don't submit answers to these questions, but the self-assessment in your written reflection asks about this step. Keep your answers handy: they'll help when you're troubleshooting failing tests later on.

---

### Task 2: Write Example-Based Tests

An *example-based test* runs the code on one input you chose and compares the result with the output you expect. "Example-based" describes how a test picks its inputs, not how much code it covers (its scope, from lecture). Starting in Task 3 you'll write *property-based* tests, which check a rule against many generated inputs instead.

Add tests to `tests/test_normalize.py` and `tests/test_search.py`. Each file has `TODO (Task 2)` comments with ideas.

**In `tests/test_normalize.py`:**
- Tests for words with diacritics in `normalize_document` (e.g., "naïve", "résumé")
- Tests for hyphenated words in `normalize_document` (what does "co-op" produce?)
- Tests for "C++" and "node.js"
- At least two more consistency tests in `TestNormalizationConsistency`

**In `tests/test_search.py`:**
- At least two more search tests, for example that "résumé" finds the resume tips document, or that a two-word query returns the right document

**Requirements for Task 2:**
- At least 6 new tests across the two files (CI's test-quality job counts them)
- At least two of them involve diacritics or hyphens
- Each test asserts something specific, not just "the result is not empty"

Some of your new tests may fail until Task 6. That's expected.

---

### Task 3: Implement `check_property`

Open `tests/pbt/checker.py` and implement `check_property`. Its docstring says exactly what it should do.

**A correct implementation is about 10 lines.** You don't need shrinking, statistics, or any imports beyond `random`.

To try it by hand, start `python` in the container terminal and run:

```python
import sys; sys.path.insert(0, 'tests')
from pbt.checker import check_property

def gen(rng): return rng.randint(0, 100)
def prop_small(n): return n < 50

passed, ce = check_property(prop_small, gen, trials=200, seed=42)
print(passed, ce)   # should print False and a number >= 50
```

When it's done, the checks in `tests/grading/test_checker.py` pass (`make grade`), and the three PBT tests in `test_properties.py` run instead of raising `NotImplementedError`. Some of them may still fail; Tasks 5 and 6 deal with that.

---

### Task 4: Define a New Property

Open `tests/pbt/test_properties.py`. It imports properties from `tests/pbt/properties.py` and tests them with `check_property`.

`tests/pbt/properties.py` provides four properties:

- `prop_idempotent_document`: `normalize_document` is *idempotent*, meaning a second pass changes nothing. Normalize a text, join the tokens with spaces, and normalize that string: you get the same tokens back.
- `prop_no_empty_tokens_document` and `prop_no_empty_tokens_query`: neither normalizer ever returns an empty string as a token.
- `prop_query_document_consistent`: the two normalizers are *consistent*, meaning `normalize_query` and `normalize_document` return the same tokens for the same text.

**What to do:**

1. Run `make test` and see which properties pass or fail with the provided, naive generators.

2. **Define at least one new property** in `test_properties.py`: a `prop_` function that takes a string and returns `True` or `False`. It should check something the four provided properties don't.

3. **Add at least one new test class** that uses `check_property` with your property and a generator of your choice. Pick the generator most likely to find a failure, if there is one.

Your property should be precise enough to catch a real bug. A property like "the result is a list" holds whether the normalizer works or not.

---

### Task 5: Write Domain-Aware Generators

**Step 1: write the generators.**
Open `tests/pbt/generators.py`. The two placeholder generators, `diacritic_word` and `hyphenated_phrase`, return plain random words. Replace each one with a real implementation.

**`diacritic_word`**: words containing letters with diacritical marks: accents (é, è, ê, à, â, î, ô, ù, û), but also the diaeresis (ë, ï, ü), the cedilla (ç), the tilde (ñ), and others. You could add diacritics to random words, or combine a list of real words with random changes.

**`hyphenated_phrase`**: compound words joined by hyphens (co-op, well-known, state-of-the-art). You could join two or more random words with hyphens. Also think about what else can sit on either side of a hyphen in real text.

The checks in `tests/grading/test_generators.py` look at the *shape* of what your generators produce: enough output with diacritics or hyphens, several kinds of diacritical mark, more than one hyphen in some phrases, and many distinct outputs. A generator that only repeats a short list of words you thought of can only test inputs you already thought of.

Passing those checks doesn't mean your generators find bugs. When you submit, the autograder also runs your generators against versions of `normalize_query` with bugs you haven't seen, and checks whether the consistency property fails on the inputs they produce. If it doesn't, the feedback shows you an input that does expose the bug, next to some inputs your generator produced. Use it to work out what your generator is missing. Adding our input alone won't pass: the check only counts inputs other than ours.

We can't give you these checks to run locally, because the buggy versions would show you exactly which inputs to generate. The point isn't to catch you out. Developers often have to write tests for a *black box*, a system whose code they can't see, and working out what to try from the outside is a real skill.

**Step 2: test with the generators.**
Add two consistency tests to `test_properties.py`, one that uses `diacritic_word` and one that uses `hyphenated_phrase`. Each of them should find a failure on the starter code. Keep them failing for now: Task 6 starts from the counterexamples they report.

Naive generators (random lowercase words) rarely produce the inputs that make normalization hard. Knowing what makes this domain hard is what makes these generators useful.

---

### Task 6: Regression Tests and Bug Fixes

**Part A: Regression tests**

After Task 5, `check_property` should be finding failures of the consistency property on inputs with diacritics or hyphens.

**Step 1: pick a counterexample and minimize it.**
Take the failing input that `check_property` returned, and look for a shorter or simpler input that still fails the same way. If it's several words, try one. If it has extra letters, try removing some.

This is *manual counterexample minimization*: you're doing by hand what a shrinking algorithm does automatically. You'll see one in Task 7.

**Step 2: write a regression test that records both.**
A *regression test* keeps a bug you've already found from coming back. It runs the exact input that failed, so if a later change brings the bug back (a *regression*), the test fails again.

Add at least two regression tests (one for each bug) to the `# Regression tests` section at the end of `test_properties.py`. Each test should:
- Use a specific failing input directly (not call `check_property`)
- Record the original counterexample and your minimized version in its docstring
- Include the generator name and seed, so a future reader knows how the failure was found

Use this docstring format so graders can find your work quickly:

```python
def test_regression_naïve_consistency() -> None:
    """Regression: query/document normalization mismatch.

    Original counterexample : 'naïveté' (diacritic_word generator, seed=7)
    Minimized counterexample: 'naïve'

    Minimization: any single letter with a diacritic reproduces the bug;
    the extra suffix was irrelevant.
    """
    assert prop_query_document_consistent("naïve"), (
        "naïve: document folds the diaeresis to 'naive', query must do the same"
    )
```

**Part B: Fix the two bugs**

Fix the two bugs in `normalize_query` in `src/searchengine/normalize.py`. Compare it line by line with `normalize_document`: there are exactly two differences, and each one is a bug.

Fix one bug at a time, and check each fix:
- After the first fix, run `search explain "naïve"`. Do the document and query results agree now?
- After the second, run `search explain "co-op"`.

When both are fixed, the four originally failing tests, your regression tests, and the Task 6 grading checks (`TestBugsFixed` in `make grade`) pass.

---

### Task 7: Hypothesis

[Hypothesis](https://hypothesis.readthedocs.io/) is a property-based testing library: a mature version of what you built in Tasks 3 and 5. You describe the kind of input you want with a *strategy* (for example, `st.text()` for any string), and Hypothesis generates the inputs, runs your test on each one, and, when one fails, shrinks it to a small failing example for you.

1. **Read the example.** Open `tests/pbt/test_hypothesis.py`. It has one complete Hypothesis test, which uses a provided property. Run `make test` and find it in the output.

2. **Write two Hypothesis tests**, one for `prop_idempotent_document` and one for `prop_query_document_consistent` (both described in Task 4), using `st.text()`. Hypothesis tries 100 inputs per test by default. Ask for 2000 instead, by adding a `@settings` line above `@given` (and adding `settings` to the import):

   ```python
   @settings(max_examples=2000)
   @given(st.text())
   def test_...(text: str) -> None:
       ...
   ```

   The bug you're about to find shows up in only a small share of random strings, and 100 tries usually miss it.

3. **Run `make test`.** One of your new tests should fail, even though Task 6 fixed both bugs. Hypothesis prints a `Falsifying example:` with the input it found. It also saves that input in the `.hypothesis/` folder and tries it first on the next run, so the test keeps failing until the bug is fixed. (If neither test fails, run `make test` again.)

   This bug was not planted. It was in this code when it was used last semester, and the course staff's own tests didn't find it.

4. **Understand the failure before fixing it.** Some of the characters Hypothesis finds look like ordinary letters. Start `python` in the container terminal and run this, with the input from `Falsifying example:` in place of `___` (quotes included):

   ```python
   import unicodedata
   from searchengine.normalize import normalize_document

   s = ___
   for c in s:
       print(repr(c), unicodedata.name(c, "(no name)"))

   first = normalize_document(s)
   print(first)
   print(normalize_document(" ".join(first)))
   ```

   The first loop prints the Unicode name of each character. The last two lines show the first and second normalization passes. Which step of normalization produces the difference?

5. **Write a regression test** in `test_hypothesis.py`: a plain test (not a Hypothesis test) with the input Hypothesis gave you. Use this docstring format:

   ```python
   def test_regression_<descriptive_name>() -> None:
       """Regression: <what went wrong>.

       Found by        : Hypothesis, <your test's name> (st.text(), 2000 examples)
       Hypothesis gave : '<the input>' (<its Unicode name>)

       <What the two normalization passes produced, and why.>
       """
   ```

6. **Fix the bug** in `normalize.py`. The two normalizers must still agree with each other, and your consistency test will tell you if they don't.

When you're done, your Hypothesis tests, your regression test, and the Task 7 grading checks (`TestHoldsForAnyText` in `make grade`) pass. Those grading checks run Hypothesis themselves. When they fail they don't print the input, because finding it is your tests' job.

> **Random or repeatable?** Each time you run `make test` in your container, Hypothesis tries a different 2000 strings. Over many runs your tests try far more inputs than any single run does. A failure, once found, is saved in `.hypothesis/` and tried first next time, so you can still reproduce it (compare the `seed` parameter of your `check_property`). The cost is that the same code can pass one run and fail the next. *Software Engineering at Google* (ch. 11) calls tests like that flaky, and explains why a team stops trusting a suite that has them.
>
> So when Hypothesis detects that it's running in CI (GitHub Actions tells it), it fixes its seed and stops using saved failures: every CI run tries the same inputs. The `TestHoldsForAnyText` grading checks fix their seed the same way, with `derandomize=True`. A fixed seed makes a result repeatable, but it also means the same 2000 strings get tried on every run, and no others. One consequence: your own tests can pass in your container and fail in CI, or the other way around.

---

### Task 8: Mutation Testing

In HW2 Task 5 you checked whether one test could tell your constraint from its absence. Mutation testing asks that question of a whole test suite. A tool called **mutmut** makes many small changes to `normalize.py`, one at a time (for example `==` to `!=`, a string replaced by `"XXXX"`, or a function call removed). Each changed version is called a **mutant**. mutmut runs your tests against each one. If a test fails, the mutant is **killed**. If every test still passes, the mutant **survived**: your tests can't tell that version of the code from the real one.

You'll run mutmut twice, first without your Hypothesis tests and then with them. Finish Tasks 6 and 7 first, since mutants of buggy code are hard to interpret.

1. **Run mutmut without your Hypothesis tests.** It takes a few seconds:

   ```bash
   make mutmut          # saves mutmut_results.txt
   make results         # lists the surviving mutants
   mutmut show <name>   # shows what one mutant changed
   ```

   `make mutmut` passes pytest the option `-m "not hypothesis"`, which skips every test marked `@given`. Your other tests in `test_hypothesis.py`, such as your regression test, still run.

2. **Analyze the survivors** in [MUTANTS.md](MUTANTS.md), up to two of them. For each one, decide whether it's a **real gap** (some input would make the search engine behave differently, and none of your tests tries it) or makes **no observable difference** (no input could tell it from the original code), and explain why it survived.

3. **Kill one of them** with a new example-based test (as in Task 2) in `tests/test_normalize.py` or `tests/test_search.py`. Add a line to its docstring naming the mutant:

   ```python
   def test_...() -> None:
       """<What this test checks.>

       Kills mutant: searchengine.normalize.x_normalize_query__mutmut_3
       """
   ```

   Then run `make kills`. It runs mutmut on that one mutant twice, with your new test and without it, still leaving out your Hypothesis tests. The claim holds if the mutant is killed the first time and survives the second. The autograder runs the same check.

   If no mutant survived step 1, your earlier tests already catch every change mutmut tries. Say so in MUTANTS.md, and put the `Kills mutant:` line on an existing test instead, naming a mutant that only that test kills. `make kills` tells you whether you found one.

4. **Run mutmut with all your tests**, and finish MUTANTS.md:

   ```bash
   make mutmut-all      # saves mutmut_results_all.txt
   ```

   Compare the two runs. Which of your Hypothesis tests killed the mutants that survived step 1, and why could it when your other tests couldn't?

5. **Run `make mutmut` once more**, so `mutmut_results.txt` reflects your final tests. Then commit `MUTANTS.md`, `mutmut_results.txt`, and `mutmut_results_all.txt`.

---

## Task Summary

| Task | Type | Files | Description |
|------|------|-------|-------------|
| 1 | Orientation | (read only) | Understand the system before testing it |
| 2 | Tests | `test_normalize.py`, `test_search.py` | At least 6 example-based tests |
| 3 | Implement | `tests/pbt/checker.py` | `check_property` |
| 4 | Tests | `tests/pbt/test_properties.py` | A new property and a test class for it |
| 5 | Generators | `tests/pbt/generators.py`, `test_properties.py` | Domain-aware generators, and tests that use them |
| 6 | Tests + fix | `test_properties.py`, `normalize.py` | Regression tests, then fix the two bugs |
| 7 | Tests + fix | `tests/pbt/test_hypothesis.py`, `normalize.py` | Hypothesis tests, a regression test, then fix the third bug |
| 8 | Evaluation | `MUTANTS.md`, a test file, `mutmut_results*.txt` | Analyze surviving mutants, kill one, then compare with Hypothesis |

---

## Tips

- Run `search explain "<text>"` often. If the document and query columns disagree, searches for that text fail silently.
- Fix bugs one at a time and check each fix before moving on.
- Don't edit `tests/grading/`, `tests/pbt/properties.py`, `pyproject.toml`, or `.github/workflows/ci.yml`. The autograder uses its own original copies, so edits there won't change your results.

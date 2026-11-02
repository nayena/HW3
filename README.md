# HW3: Testing a Search Engine

This assignment is a small, working (but buggy) search engine over eight text documents. Its normalizer, the code that turns documents and queries into searchable words, is the center of the assignment. You'll write tests that find its bugs, build a small version of a property-based testing tool and then use a real one, and finally test your tests.

**ASSIGNMENT DUE DATE (all parts):** Monday, Nov 2nd @ 11:59pm ET

## Learning Objectives

By completing this assignment, you will:

1. **Find out what a system is supposed to do before testing it**, by reading its code and probing it, and state that as specific expectations (Tasks 1 and 2)
2. **Write tests as general claims about behavior**, not only as single examples, and see what each kind can and can't catch (Tasks 2, 4, and 7)
3. **Choose and generate test inputs**, and see how the inputs you try decide which bugs you can find (Tasks 3, 5, and 7)
4. **Turn a failure into understanding**: shrink a failing input to what matters and keep it as a regression test (Tasks 6 and 7)
5. **Compare a tool you built with a mature one for the same job**, and say what the mature tool does that yours doesn't (Task 7)
6. **Measure how good a test suite is**, by checking whether it notices small deliberate changes to the code (Task 8)

## Tests as claims

Every test you write in this assignment is a claim about what "correct" means for the search engine. Each task hands more of the work of checking that claim to a tool:

| Tool | What you write | What the tool does |
|---|---|---|
| pytest | An input and the output you expect | Runs each example and reports failures |
| Your `check_property` | A property, and a generator for inputs | Tries many generated inputs and reports the first failure |
| Hypothesis | A property, and a description of the inputs | Generates inputs, shrinks a failure to a small example, and remembers it |
| mutmut | Nothing new | Makes small changes to the code and checks whether your tests notice |

The search engine runs, and most searches work. Some don't, and nothing tells you so. [ARTIFACT.md](ARTIFACT.md) starts by having you explore it before you test anything.

---

## CI/CD

**Continuous Integration / Continuous Delivery (CI/CD)** refers to the practice of automatically running checks (linting, tests) whenever code changes are pushed to a shared repository. In this project, CI is implemented with **GitHub Actions**, which defines a set of automated jobs in a workflow file ([`ci.yml`](.github/workflows/ci.yml)). Each job runs inside the same Docker image you develop in, and Gradescope runs the same checks when you submit. As in HW1 and HW2, reading the workflow file is the most reliable way to know exactly which commands CI runs.

### Running CI on GitHub

In most projects, CI runs automatically every time someone pushes. **In this course it only runs when you start it yourself.** Your repository is private, and GitHub Actions minutes for private repositories come out of your personal GitHub account's free monthly quota, which you may need for other courses. So do your checking in the container (`make check`), and run CI on GitHub when you want to confirm your pushed work.

1. Push your commits to GitHub.
2. On your repository's GitHub page, open the **Actions** tab.
3. Choose the **CI** workflow in the list on the left.
4. Click **Run workflow**, keep the branch set to `main`, and click the green **Run workflow** button.
5. After a few seconds a new run appears; click it to watch each job and read its output.

Each run uses a few minutes of your quota, so run it when you have something to confirm, not after every commit. The comments at the top of [`ci.yml`](.github/workflows/ci.yml) show what the usual automatic trigger looks like.

---

## Assignment Structure

This assignment has three parts:

| Part | Where | Description |
|------|-------|-------------|
| **Artifact** | [ARTIFACT.md](ARTIFACT.md) | Test the search engine, fix its bugs, and test your tests; submitted to **HW3 Artifact** on Gradescope |
| **Written Reflection** | [WRITTEN.md](WRITTEN.md) | Reflect on your process and connect it to the readings; submitted to **HW3 Written** on Gradescope |
| **AI Usage Report** | [HW3 AI usage reporting tool](https://genai.cs.brandeis.edu/prompt/014a54ef-3e1c-406e-9353-66c65ec246d5) | Required **even if you didn't use AI** |

**Complete the artifact first**, then write your reflection. The written component asks you to reflect on your experience completing the artifact, so it should be done after the artifact.

AI usage reporting should come last. Full instructions for reporting AI usage can be found on Moodle.

---

## Required Reading

Before starting the written reflection, read:

- **Edsger W. Dijkstra, "The Humble Programmer"** (EWD 340, ACM Turing Award Lecture, 1972), provided on Moodle
- **Adam Bender, "Testing Overview"**, Chapter 11 of *Software Engineering at Google* (Titus Winters, Tom Manshreck, and Hyrum Wright, eds., 2020), provided on Moodle

This reading is essential for the written reflection.

---

## Prerequisites & Setup

### Getting your repository

You work in your own **private** copy of the assignment:

1. Go to <https://github.com/brandeis-cosi-106b/hw3-fa26> and click **Use this template → Create a new repository**.
2. Set **Owner** to your own GitHub account, name it (for example `cosi106b-hw3`), and choose **Private**. Your repository must be private, since public repositories let other students see your work.
3. Click **Create repository**, then clone *your* new repository (not `brandeis-cosi-106b/hw3-fa26`) to your computer.

Your copy starts with a single commit and isn't linked to the course repository, so it won't receive changes automatically. See [Required updates](#required-updates) for how to get them.

### Required updates

If bugs in the assignment are discovered after release, course staff may publish fixes. **Applying them is required.** They will be announced with one or more commit IDs. In your repository, inside the container terminal:

```bash
git remote add upstream https://github.com/brandeis-cosi-106b/hw3-fa26.git   # first time only
git fetch upstream
git cherry-pick <commit-id>          # as announced
git push
```

If Git reports a conflict, it's because you edited the same lines as the fix. Open the listed files, keep both your work and the fix, then run `git add <file>` and `git cherry-pick --continue`. Don't use `git merge` or `git pull` with `upstream`: your repository shares no history with it, so every file you changed would conflict. The Gradescope autograder always checks against the updated version, so a fix you skip can make it fail.

### Tools

As in HW1 and HW2, all work happens inside a **Docker development container** with every tool preinstalled (Python 3.11, Make, pytest, Hypothesis, mutmut, ruff, and click), at exactly the versions that GitHub Actions and Gradescope use. You **don't** need to install any of them yourself.

**Follow [DOCKER.md](DOCKER.md) to get set up.** If you set up Docker Desktop and VS Code for HW1, you already have everything; open this repository in its container the same way. If Docker won't run on your computer, DOCKER.md describes a browser-based fallback.

Once your container is open, check in its terminal that everything is there:

```bash
make help
search --help
mutmut --version
```

> **Prefer to install tools natively?** You can, but it's unsupported: if your
> results differ from CI or Gradescope, the container is the reference. The
> exact versions are pinned in [`uv.lock`](uv.lock) and
> [`.devcontainer/install-tools.sh`](.devcontainer/install-tools.sh).

### The Makefile, and where the packages come from

As in HW1, the [Makefile](Makefile) gives short names to the commands you'll run most. Each target is one or two plain commands, so you can read it to see exactly what runs.

| Command | What it does |
|---|---|
| `make test` | Run the test suite (your tests and the provided ones) |
| `make lint` | Lint `src/` with ruff |
| `make grade` | Run the grading checks in `tests/grading/` |
| `make check` | Lint, test, and grade: the same checks CI runs |
| `make mutmut` | Run mutation testing without your Hypothesis tests and save `mutmut_results.txt` (Task 8) |
| `make mutmut-all` | Run mutation testing with all your tests and save `mutmut_results_all.txt` (Task 8) |
| `make results` | List the mutants that survived the last mutmut run |
| `make kills` | Check the mutants your tests claim to kill (Task 8) |
| `make clean` | Remove caches and mutmut's working files |

The search engine has its own command, `search`, with three subcommands: `search search "query"`, `search list-docs`, and `search explain "text"`.

The Python packages were installed into the container with **uv**, a Python package and project manager. It reads [`pyproject.toml`](pyproject.toml) for the packages the project needs and [`uv.lock`](uv.lock) for their exact versions, the same jobs `package.json` and `package-lock.json` did for npm in HW2. You won't need to run uv yourself in this assignment.

---

## Architecture

```
src/searchengine/
  corpus.py       loads the documents from corpus/docs/
  normalize.py    turns text into searchable words (the center of this assignment)
  stopwords.py    common words that are left out of the index
  index.py        the inverted index: which documents contain each word
  search.py       answers a query from the index
  cli.py          the `search` command
corpus/docs/      the eight documents
tests/
  test_normalize.py    example-based tests for normalization (Task 2)
  test_search.py       example-based tests for search (Task 2)
  pbt/
    checker.py         your property-based testing tool (Task 3)
    generators.py      input generators (Task 5)
    properties.py      the provided properties (do not modify)
    test_properties.py tests that use check_property (Tasks 4-6)
    test_hypothesis.py tests that use Hypothesis (Task 7)
  grading/             checks on your work, run by `make grade`
scripts/
  check_kills.py       checks your Task 8 kill claim (`make kills`)
  count_tests.py       counts your tests for CI
MUTANTS.md             your Task 8 mutant analysis
```

---

## Grading

This assignment is evaluated using **two independent letter grades**:

| Grade | Evaluates |
|-------|-----------|
| **Artifact Grade** | Technical execution, engagement with the tools, good-faith effort |
| **Reflection Grade** | Theory-building, honest self-assessment, engagement with course ideas |

These grades are **not mechanically averaged**. Strong performance in one area does not automatically make up for the other, though a strong written reflection can partially offset incomplete technical work.

**See [RUBRIC.md](RUBRIC.md) for detailed grading criteria.**

### What We're Looking For

**Artifact**: Aim for passing tests, but we also value *engagement* and *intentionality*. Does each test check something specific? Did your generators and Hypothesis tests find the bugs, or did you find them some other way and write tests afterwards? Can you explain why each surviving mutant survived, and why your Hypothesis tests killed it? The self-assessment in your written reflection helps us see this.

**Reflection**: We value honesty, specificity, and real engagement with course ideas, especially the readings for this assignment listed above. A thoughtful reflection on partial success is more valuable than a superficial reflection on complete success.

### CI Jobs

The following CI jobs run each time you run the CI workflow (see [Running CI on GitHub](#running-ci-on-github)):

1. **quality**: `ruff check src/` passes
2. **tests**: the test suite passes
3. **test-quality**: the grading checks in `tests/grading/` pass, and you added at least 6 tests
4. **mutation**: runs mutmut without and then with your Hypothesis tests, lists the surviving mutants each time, and checks your Task 8 kill claim. This job reports only; it never fails the run.

Passing all CI jobs is a strong signal of artifact completion, but it is not the sole criterion for grading.

### Gradescope Autograder

When you submit your artifact to Gradescope, it runs the **same checks** as the CI jobs above, one Gradescope test per check, and shows you the exact command and its output for each. A few things work differently from GitHub Actions:

- Every check runs, even if an earlier one fails, so you get feedback on everything at once.
- The autograder runs the **original** grading checks, properties, and settings. Editing `tests/grading/`, `tests/pbt/properties.py`, or `pyproject.toml` won't change your autograder results (and will be visible to course staff).
- Your Task 8 kill claim is checked the same way `make kills` checks it, and it counts toward the score.
- Two extra checks run your Task 5 generators against versions of `normalize_query` with bugs you haven't seen, to see whether your generators produce inputs that expose them. If they don't, the feedback shows an input that does, so you can work out what your generator is missing.
- Lint is reported but earns no autograder points, since it already passes on the starter code. **Keep it passing anyway**: it counts toward your artifact grade.

The autograder score is **not** your artifact grade. It's one piece of evidence course staff use alongside [RUBRIC.md](RUBRIC.md).

---

## AI Tools Policy

You may use automation tools to help with this assignment, including both LLM-powered tools and "older" automations (e.g., those built into your IDE). You must document your usage in the AI usage report (see [Assignment Structure](#assignment-structure)).

LLM tools can help you understand error messages, Python, and Hypothesis's API. They also tend to write tests that look right and check very little, which is the kind of weakness mutation testing (Task 8) is designed to expose.

**Remember**: LLM tools can also help you write code, but you need to understand what it's doing. You may be asked about your submission in an oral exam.

---

## Submission

Your final repository should contain:

| File | Description |
|------|-------------|
| **`tests/test_normalize.py`, `tests/test_search.py`** | Your example-based tests (Task 2) and your Task 8 kill test |
| **`tests/pbt/checker.py`** | Your `check_property` (Task 3) |
| **`tests/pbt/generators.py`** | Your generators (Task 5) |
| **`tests/pbt/test_properties.py`** | Your property, its tests, and your regression tests (Tasks 4-6) |
| **`tests/pbt/test_hypothesis.py`** | Your Hypothesis tests and regression test (Task 7) |
| **`src/searchengine/normalize.py`** | With all three bugs fixed (Tasks 6 and 7) |
| **`MUTANTS.md`**, **`mutmut_results.txt`**, and **`mutmut_results_all.txt`** | Your mutant analysis and your two mutmut runs (Task 8) |

### How to Submit

0. Review [RUBRIC.md](RUBRIC.md) to understand how you'll be evaluated
1. Complete the tasks in [ARTIFACT.md](ARTIFACT.md) (aim for `make check` and `make kills` to pass)
2. Commit and push:

```bash
git add -A
git commit -m "Complete HW3: search engine testing"
git push
```

3. Run the CI workflow on GitHub ([Running CI on GitHub](#running-ci-on-github)) and confirm all jobs pass.

4. Submit your **artifact** on Gradescope: open the **HW3 Artifact** assignment, choose **GitHub** as the submission method, and select your HW3 repository and the `main` branch. The autograder results appear within a few minutes. You can resubmit as many times as you like before the deadline; your last submission is the one graded.

5. Complete the written reflection in [WRITTEN.md](WRITTEN.md) (including the self-assessment), then upload your completed `WRITTEN.md` to the **HW3 Written** assignment on Gradescope.

6. Submit your AI usage report through the [HW3 AI usage reporting tool](https://genai.cs.brandeis.edu/prompt/014a54ef-3e1c-406e-9353-66c65ec246d5), **even if you didn't use AI**. Full instructions for reporting AI usage can be found on Moodle.

---

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [Hypothesis documentation](https://hypothesis.readthedocs.io/), especially the [quickstart](https://hypothesis.readthedocs.io/en/latest/quickstart.html) and the [strategies reference](https://hypothesis.readthedocs.io/en/latest/reference/strategies.html)
- [mutmut documentation](https://mutmut.readthedocs.io/)
- Python's [`unicodedata`](https://docs.python.org/3/library/unicodedata.html) and [`re`](https://docs.python.org/3/library/re.html) modules
- [uv documentation](https://docs.astral.sh/uv/)

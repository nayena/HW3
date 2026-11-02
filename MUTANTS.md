# Task 8: Surviving Mutants

See Task 8 in [ARTIFACT.md](ARTIFACT.md).

## Without your Hypothesis tests (`make mutmut`)

**How many mutants survived?**

Fill in one section for each surviving mutant, up to two.

### Mutant 1

**Name:** <!-- copy it from `make results`, e.g. searchengine.normalize.x_normalize_query__mutmut_3 -->

**What it changes:** <!-- paste the changed line from `mutmut show <name>`, or describe it in a sentence -->

**Real gap or no observable difference?**

**Why it survived:** <!-- 2-4 sentences. For a real gap: what input would show the difference, and why none of your tests tried it. For no observable difference: why no input could tell this mutant from the original code. -->

**Killed?** <!-- If you killed it, name the test. If not, say why not. -->

### Mutant 2

**Name:**

**What it changes:**

**Real gap or no observable difference?**

**Why it survived:**

**Killed?**

## With all your tests (`make mutmut-all`)

**How many mutants survived?**

**Which of your Hypothesis tests killed the mutants above, and why could it when your other tests couldn't?** <!-- One paragraph. -->

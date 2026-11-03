# Task 8: Surviving Mutants

See Task 8 in [ARTIFACT.md](ARTIFACT.md).

## Without your Hypothesis tests (`make mutmut`)

**How many mutants survived?**

2 of 60 (before adding the killing test below): `x_normalize_query__mutmut_19` and `x_normalize_query__mutmut_20`. Both change the same line, the step in `normalize_query` that strips punctuation. After adding `TestNormalizeQuery::test_strips_punctuation`, 0 survive (the committed `mutmut_results.txt` reflects the final suite).

### Mutant 1

**Name:** searchengine.normalize.x_normalize_query__mutmut_19

**What it changes:**
```diff
-    text = re.sub(r"[^\w\s]", "", text)
+    text = re.sub(r"XX[^\w\s]XX", "", text)
```

**Real gap or no observable difference?** Real gap.

**Why it survived:** The mutated pattern only matches the literal text `XX<punctuation>XX`, so in practice the query normalizer stops removing punctuation, while the document normalizer still removes it. Any query that has punctuation in it shows the difference: `normalize_query("node.js")` gives `['node.js']` instead of `['nodejs']`, so searching `node.js` (or `python!`, `résumé?`) silently finds nothing. None of my non-Hypothesis tests gave `normalize_query` a string containing punctuation other than a hyphen: my example tests used plain words, diacritics and hyphens, and my generators produce letters, digits and hyphens only. The provided `test_strips_punctuation` checks `normalize_document`, not the query side.

**Killed?** Yes, by `tests/test_normalize.py::TestNormalizeQuery::test_strips_punctuation` (`normalize_query("Node.js, please!") == ["nodejs", "please"]`). `make kills` confirms it: killed with the test, survived without it.

### Mutant 2

**Name:** searchengine.normalize.x_normalize_query__mutmut_20

**What it changes:**
```diff
-    text = re.sub(r"[^\w\s]", "", text)
+    text = re.sub(r"[^\w\s]", "XXXX", text)
```

**Real gap or no observable difference?** Real gap.

**Why it survived:** Instead of deleting each punctuation character in the query, the mutant replaces it with `XXXX`. Lowercasing has already happened, so the capitals stay: `normalize_query("node.js")` gives `['nodeXXXXjs']`, which no document token can ever equal. As with mutant 1, the gap is that no non-Hypothesis test sent punctuation through `normalize_query`, so every test input took the same path through this line in the original and the mutant (the pattern never matched anything).

**Killed?** Yes, by the same test, `TestNormalizeQuery::test_strips_punctuation`. It has the claim line for mutant 1 only, since one claim is needed; that test fails on this mutant too.

## With all your tests (`make mutmut-all`)

**How many mutants survived?**

0 of 60.

**Which of your Hypothesis tests killed the mutants above, and why could it when your other tests couldn't?**

`test_query_document_consistent_any_text` (the Hypothesis test for `prop_query_document_consistent` over `st.text()`) kills both mutants on its own. Run against either mutant, it reports `Falsifying example: text=':'`. The document side gives `[]` and the query side gives `[':']` (or `['XXXX']`). My other tests only tried inputs I designed for the bugs I already knew about (diacritics and hyphens), so my generators produce letters, digits and hyphens and never punctuation. `st.text()` isn't aimed at any particular bug. It draws from all of Unicode, and punctuation turns up in a large share of its strings, so the first few hundred examples include it. Hypothesis then shrinks the failure to one colon. The Hypothesis test also checks a *relation* (query equals document) rather than a fixed expected output, so it needs no hand-written answer for each input. That is why it can try 2000 arbitrary strings, while my example tests could only check inputs whose correct output I had worked out in advance.

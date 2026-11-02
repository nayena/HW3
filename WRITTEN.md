# HW3 Written Reflection

Answer the following questions thoughtfully. There are no "right" answers. The goal is honest reflection on your experience and on the ideas from class.

This written component is designed to reward **honest engagement and theory-building**, even if your artifact is incomplete. A test suite that passes without understanding and a partial test suite with deep understanding are *not* the same thing, but both can be discussed thoughtfully here.

---

## Part 0: Self-Assessment

Complete this section **before** writing your reflection. Be honest. This is not penalized, and it helps us calibrate grading. Accurate self-assessment demonstrates the kind of self-awareness we value.

### Artifact Completion

For each task, mark your status: **Done**, **Partial**, or **Not Done**. Add brief notes if helpful.

| Task | Status | Notes (optional) |
|------|--------|------------------|
| 1. Read the code and tried `search explain` before writing tests | | |
| 2. At least 6 new example-based tests | | |
| 3. `check_property` implemented | | |
| 4. A new property, with a test class that uses it | | |
| 5. `diacritic_word` and `hyphenated_phrase` implemented | | |
| 6. Regression tests with minimized counterexamples; both bugs fixed | | |
| 7. Hypothesis tests, a regression test, and the third bug fixed | | |
| 8. Surviving mutants analyzed, one killed by a named test, and compared with Hypothesis | | |
| All tests pass (`make test`) | | |
| Lint passes (`make lint`) | | |
| Grading checks pass (`make grade`) | | |

### Understanding Self-Check

Answer briefly (1–3 sentences each):

1. **What do you feel you genuinely understand** about this assignment? (Not just "made it work," but could explain to someone else or extend on your own.)

2. **What did you make work without fully understanding?** (Be honest. This is useful self-knowledge.)

3. **Where did you get stuck?** What did you try before moving on or seeking help?

---

## Part 1: Short Response (1–2 paragraphs each)

### A: Shrinking by Hand and by Hypothesis

In Task 6 you took a failing input from `check_property` and shrank it yourself. In Task 7, Hypothesis handed you a failing input it had already shrunk. Compare the two minimizations, giving the original and minimized input from Task 6 and the input Hypothesis reported in Task 7, and explain what each one told you about the bug behind it. Was the smallest input always the easiest one to understand?

### B: Generic and Domain-Aware Inputs

Your Task 5 generators were built from what you knew about this domain (diacritics and hyphens), and they found the two Task 6 bugs. Hypothesis's `st.text()` knows nothing about search engines, and in Task 7 it found a third bug that your generators never produced an input for. Using these results, explain where knowing the domain helped you choose test inputs and where it limited you.

### C: Mutation Testing as Test Evaluation

*Software Engineering at Google* (ch. 11) says that tests have no tests of their own, so they need a person to review them, and it warns that code coverage only shows that a line ran, not that anything checked the result.

What did mutation testing reveal about your test suite that you could not have known from simply running the tests, and what does it mean to "strengthen" a test suite?

### D: What Counts as Correct?

The normalizer makes choices about what users can find. A few cases:

- Before Task 6's fix, a search for "co-op" became "coop" and would match a page about chicken coops. After the fix, it becomes "co" and "op", and a search for "coop" no longer finds the co-op programs document.
- A search for "The Who" drops "the" as a stopword and becomes a search for "who", which matches any document with that word in it.
- A post written in styled letters like 𝐁𝐫𝐞𝐚𝐤𝐢𝐧𝐠 𝐍𝐞𝐰𝐬 (common on social media) is indexed differently from plain text, at least until Task 7's fix.
- A spam post written in l33tsp34k, like "fr33 g1v34w4y", is indexed as the words "fr33" and "g1v34w4y", so a search for "free giveaway" never finds it. Spammers spell words this way on purpose, to get past filters that look for "free".

Choose one of these cases (or another you found) and argue what the search engine should do, and who should get to decide.

---

## Part 2: Essay on the Limits and Value of Testing (500–700 words)

*This is the biggest question, in terms of both size and importance. Take your time with it.*

Write an essay that engages with **both** readings, Dijkstra's "The Humble Programmer" and *Software Engineering at Google* (ch. 11), using your own experience in this assignment as evidence. Your essay should take a position, not just describe both arguments neutrally.

**Possible directions** (choose 2–3 to develop; you do not need to touch all of them):

- **What your suite shows and what it doesn't**: what your finished tests leave unchecked, and whether that matters for a search engine like this one.
- **A bug nobody planted**: what the Task 7 bug says about tests written by people who already know where the bugs are, and whether Dijkstra's structural approach would have caught it.
- **Who tests the tests**: mutation testing checks your tests, but something has to check the mutation tests. What this regress says about how much any amount of testing can establish.
- **Confidence to change**: what automated tests did for the GWS team in ch. 11, and whether that is the right goal for testing, judged by how you felt changing `normalize.py` with and without your tests in place.

A thoughtful argument that testing matters less than either reading suggests is **entirely acceptable** if it is well reasoned and grounded in your experience.

---

## Submission

The written reflection is submitted separately from your artifact:

1. Write your responses in this document (or a copy of it, in any editor you like).
2. Upload the completed `WRITTEN.md` to the **HW3 Written** assignment on Gradescope.

### Formatting Guidelines

- **For all parts:** Aim for and prioritize clarity and honest engagement.
- **Part 1**: ~1–2 paragraphs each
- **Part 2**: **~500–700 words** (roughly one single-spaced page). It's fine to go slightly over.

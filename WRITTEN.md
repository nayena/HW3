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
| 1. Read the code and tried `search explain` before writing tests | Done | Claude ran `search explain` and summarized the code; I read the summary and the `naïve` / `co-op` outputs |
| 2. At least 6 new example-based tests | Done | 14 new tests (11 in test_normalize.py, 3 in test_search.py), written by Claude (AI assistant) at my direction |
| 3. `check_property` implemented | Done | Implemented by Claude |
| 4. A new property, with a test class that uses it | Done | Two properties: hyphen acts as a word break in queries; query tokens have no diacritics |
| 5. `diacritic_word` and `hyphenated_phrase` implemented | Done | Implemented by Claude; local shape checks pass, hidden autograder check not yet seen |
| 6. Regression tests with minimized counterexamples; both bugs fixed | Done | `'muÏ'` → `'ï'`, `'Ex-dlsbqgbcn;'` → `'x-y'` |
| 7. Hypothesis tests, a regression test, and the third bug fixed | Done | Bug found with `'℠'` (SERVICE MARK) |
| 8. Surviving mutants analyzed, one killed by a named test, and compared with Hypothesis | Done | See note in Self-Check 3 about trimming tests so a mutant could survive |
| All tests pass (`make test`) | Done | 53 passed (run locally with uv, not in the container) |
| Lint passes (`make lint`) | Done | |
| Grading checks pass (`make grade`) | Done | 24 passed |

### Understanding Self-Check

Answer briefly (1–3 sentences each):

1. **What do you feel you genuinely understand** about this assignment? (Not just "made it work," but could explain to someone else or extend on your own.)

   I understand the three bugs and why each one broke search. The query normalizer skipped diacritic folding, it deleted hyphens instead of turning them into spaces, and the document normalizer lowercased *before* folding (so did the query side once we copied that order in Task 6), so `℠` turned into capital `SM` after lowercasing had already run. I also understand the core idea of property-based testing: you state a rule, like "query and document agree", instead of writing down one expected output.

2. **What did you make work without fully understanding?** (Be honest. This is useful self-knowledge.)

   Most of the implementation. I used Claude Code (an AI assistant) for the artifact. It wrote the code and tests, and I followed its explanations and made the decisions it asked me about. I couldn't write the generators from scratch (especially building every accented letter from Unicode combining marks), and I don't fully understand how mutmut chooses and runs its mutants.

3. **Where did you get stuck?** What did you try before moving on or seeking help?

   Task 8. The first `make mutmut` run killed all 60 mutants, and each mutant was killed by at least two tests, so no single test could claim a kill that held. The only way to make a claim hold was to make the suite *weaker*: I chose to remove two of my own redundant tests and to drop punctuation from my generators. That left two survivors, and then I added one test to kill them. It felt backwards to weaken tests to satisfy a check about strong tests, and I come back to that in Part 1C.

---

## Part 1: Short Response (1–2 paragraphs each)

### A: Shrinking by Hand and by Hypothesis

In Task 6 you took a failing input from `check_property` and shrank it yourself. In Task 7, Hypothesis handed you a failing input it had already shrunk. Compare the two minimizations, giving the original and minimized input from Task 6 and the input Hypothesis reported in Task 7, and explain what each one told you about the bug behind it. Was the smallest input always the easiest one to understand?

In Task 6, `check_property` reported `'muÏ'` (diacritic_word, seed 7) and `'Ex-dlsbqgbcn;'` (hyphenated_phrase, seed 7). Shrinking by hand meant removing one thing at a time and checking whether it still failed. `'mu'` passed and `'Ï'` failed, so the accent was the whole cause, and `'ï'` was the minimum. For the hyphen bug, the capital letter, the `;`, and the long second part were all irrelevant, so it came down to `'x-y'`. What surprised me was the inputs that *passed*: `'x-'` and `'-y'` normalize the same way on both sides, because there is nothing on the other side to glue on. So shrinking by hand told me more than the minimum input. It told me the bug needs a word on *both* sides of the hyphen. A shrinker only gives you the end point, not the list of things that didn't fail.

Hypothesis reported `'℠'`, one character that was already minimal. It was the smallest input of the three but the hardest to understand: it looks like a symbol, not a letter, and on its own it explains nothing. It only made sense after printing its Unicode name (SERVICE MARK) and comparing the two passes, `['SM']` and then `['sm']`. That showed that NFKD decomposition *creates* uppercase letters, so lowercasing before folding leaves them uppercase. So no, the smallest input was not always the easiest to understand. `'x-y'` was easy because I already knew what a hyphen was supposed to do. `'℠'` was small because the bug is small, a single wrong order of two lines, but understanding it took knowledge about Unicode that the input itself doesn't show.

### B: Generic and Domain-Aware Inputs

Your Task 5 generators were built from what you knew about this domain (diacritics and hyphens), and they found the two Task 6 bugs. Hypothesis's `st.text()` knows nothing about search engines, and in Task 7 it found a third bug that your generators never produced an input for. Using these results, explain where knowing the domain helped you choose test inputs and where it limited you.

Knowing the domain helped because the naive generators could not find these bugs at all. `random_word` produces only lowercase ASCII, so it can never produce a hyphen or an accent, and `test_consistency_random_words` passed on the buggy code. Building generators around what makes text normalization hard (accented letters, uppercase, hyphens with stopwords or numbers on either side) is what made the consistency property fail. Domain knowledge also made the failures easy to read. A failure on `'muÏ'` points straight at diacritics.

It limited me in two ways. First, the generators only produced the categories of input I already had in mind, so they could only confirm suspicions I already had. `'℠'` is not a "diacritic" or a "hyphen". It's a symbol, so it was outside both generators by design. My diacritic generator even included compatibility letters like `ﬁ` and `Ǆ` that go through the same NFKD step, but they are *letters*: `lower()` already lowercases them before folding, so they can't expose the bug. `℠` has no lowercase form, so `lower()` skips it and its capitals only appear afterward. To check, I ran both of my generators against the idempotence property on the old line order, 5,000 inputs each, and they found nothing. The domain categories I designed around were exactly the wrong ones for this bug. Second, Task 8 showed a gap I hadn't thought about at all. Without the Hypothesis tests, nothing sent ordinary punctuation through `normalize_query`, so two mutants that broke punctuation stripping survived. `st.text()` killed both with the one-character input `':'`. So domain knowledge is good at *aiming* tests at known risks, and generic generation is good at covering everything *else*. A suite needs both, because the bugs nobody planted are, almost by definition, outside what the testers already thought about.

### C: Mutation Testing as Test Evaluation

*Software Engineering at Google* (ch. 11) says that tests have no tests of their own, so they need a person to review them, and it warns that code coverage only shows that a line ran, not that anything checked the result.

What did mutation testing reveal about your test suite that you could not have known from simply running the tests, and what does it mean to "strengthen" a test suite?

Running the tests only told me they passed. As the chapter puts it, "there are no tests for the tests themselves." Mutation testing is a way to test them anyway: it told me which *behaviors* they actually check. In the step-1 run (without Hypothesis), `x_normalize_query__mutmut_19` changed the punctuation regex to `XX[^\w\s]XX`, so queries kept their punctuation, and `__mutmut_20` replaced each punctuation mark with `XXXX`. Both survived. Searching `node.js` would silently return nothing, and every test still passed. Coverage would have reported that line as 100% covered, because every query test ran it. But none of the inputs contained punctuation, so the line never *did* anything that a test then checked. That is exactly the gap the Google chapter describes: "code coverage only measures that a line was invoked, not what happened as a result." The kill matrix also showed how my tests overlapped. The `fold_diacritics` mutants that stop stripping combining marks (`mutmut_12`–`14`) are killed only by the two direct `fold_diacritics` tests. Through `normalize_document` they make no difference, because the later punctuation regex happens to strip combining marks too.

So "strengthening" a suite doesn't mean adding more tests. It means adding tests that tell apart programs that behave differently: each test should be able to fail on some plausible wrong version of the code. My own experience complicates this. My first suite killed every mutant, and to satisfy the "one test kills one mutant" check I had to remove redundant tests and make my generators narrower. The suite got weaker by the measure that matters (fewer behaviors checked) and looked better by the check's measure. The Google chapter describes the same trap with coverage: once 80% becomes the target, "instead of treating 80% like a floor, engineers treat it like a ceiling." It argues that answering "do we have enough tests?" "with a single number ignores a lot of context," and mutation score is no exception. It is a tool for finding blind spots, like the punctuation gap, not a target to optimize.

### D: What Counts as Correct?

The normalizer makes choices about what users can find. A few cases:

- Before Task 6's fix, a search for "co-op" became "coop" and would match a page about chicken coops. After the fix, it becomes "co" and "op", and a search for "coop" no longer finds the co-op programs document.
- A search for "The Who" drops "the" as a stopword and becomes a search for "who", which matches any document with that word in it.
- A post written in styled letters like 𝐁𝐫𝐞𝐚𝐤𝐢𝐧𝐠 𝐍𝐞𝐰𝐬 (common on social media) is indexed differently from plain text, at least until Task 7's fix.
- A spam post written in l33tsp34k, like "fr33 g1v34w4y", is indexed as the words "fr33" and "g1v34w4y", so a search for "free giveaway" never finds it. Spammers spell words this way on purpose, to get past filters that look for "free".

Choose one of these cases (or another you found) and argue what the search engine should do, and who should get to decide.

I want to argue about the first two cases together, because the same mistake is behind both: the normalizer throws away information when it indexes a document, so a choice made at indexing time can't be undone at search time. Right now, after the fix, `coop` finds only the search-normalization article, because the co-op document was indexed as `co` and `op`. Before the fix, `coop` didn't find the co-op document either: the document side was always `co op`, so `coop` matched only the normalization article, and `co-op` was turned into `coop` with the same result. Neither version of the code connects the two spellings. Likewise, `The Who` returns exactly the same results as `who`, the band page and the normalization article, because `the` was never stored. The user's most specific word is the one that gets deleted.

I think the engine should **index more than one form and normalize queries less aggressively**. For hyphens, index both the split parts and the joined form (`co`, `op`, *and* `coop`), so `co-op`, `co op`, and `coop` all find the co-op document. A chicken-coop page would also match `coop`, but that is a ranking problem, and ranking can be fixed later, while a missing match never shows up in the results at all. For stopwords, keep them in the index and drop them from a query only when other words remain, so `The Who` keeps `the` and can match the exact phrase, while `the history of rock` still works like `history rock`. Who decides: not whoever happens to write `normalize.py`. Their choice looks like a technical detail, but it decides what users can find. The people who own search quality should decide, using evidence of what users actually type and whether they find it (query logs, failed searches). The consistency property we tested is necessary but not enough. Our fixed engine is perfectly consistent and still can't find the co-op page for `coop`. Consistency guarantees that both sides make the *same* choice, not that it's the right one.

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

**Proof and Confidence Are Different Jobs**

Dijkstra and the Google chapter both promise "confidence", but they mean different things by it. For Dijkstra, testing "can be a very effective way to show the presence of bugs" but is "hopelessly inadequate for showing their absence," and "the only effective way to raise the confidence level of a program significantly is to give a convincing proof of its correctness." For Google, tests make it "possible to change software with confidence." My position is that both are right because they describe different jobs: confidence that a program is correct, and confidence that a change didn't break it. The mistake is to expect testing to do the first job.

The `℠` bug is Dijkstra's argument made concrete. The course staff used this code last semester and their tests passed. They had even written the right property down: `prop_idempotent_document` was provided to us. My own domain-aware generators also found nothing when I ran them against that property on the old code, 5,000 inputs each. Every passing run was evidence, but none of it was proof, because the bug lived in a kind of input (symbols that decompose into *uppercase* letters) that nobody thought to generate. Dijkstra argues that we should "let correctness proof and program grow hand in hand" and keep programs "intellectually manageable." A proof attempt would have caught this one. To prove idempotence, you have to argue that everything the first pass outputs is already lowercase, and that is exactly the step that fails. And the actual fix came from reasoning, not from more tests. Once the two passes (`['SM']`, then `['sm']`) made the cause visible, the fix was an argument: if folding can produce uppercase letters, then lowercasing has to come after folding. That argument covers every character, which no number of tests could.

But reasoning didn't *find* the bug. Nobody had tried the proof, and Hypothesis found it with random strings that nobody aimed at the problem. The Google chapter describes the Google Web Server team, where at one point "more than 80% of production pushes contained user-affecting bugs." After a policy that all new code needed tests, run continuously, "the number of emergency pushes dropped by half" within a year. The tests didn't prove the server correct; they turned "I hope this change didn't break anything" into "anything we have tested still works." I felt that directly: when the third fix moved `lower()` below `fold_diacritics()` in *both* normalizers, it could easily have broken the Task 6 fixes or the consistency property. What made that change feel safe was the whole suite rerunning green, not any proof.

Mutation testing showed me the limit of that confidence. Without Hypothesis, two mutants that broke query punctuation survived, so for those behaviors my "confidence" was unearned: the tests ran the line but checked nothing about it. This is the regress behind "who tests the tests". Mutation testing checks the suite, but only against the kinds of mistakes mutmut knows how to make (swapped operators, `"XXXX"` strings). It would never produce the `℠` bug, which is two correct lines in the wrong order. And when I had to weaken my suite to make a single-test kill claim hold, I ran into Goodhart's law, in Marilyn Strathern's phrasing: "when a measure becomes a target, it ceases to be a good measure." The kill check was meant to *measure* whether a test adds something. Once it became a target, the cheapest way to meet it was to remove coverage, the same way Google's 80% coverage floor turned into a ceiling. Each layer of checking makes the one below it more trustworthy, but none reaches certainty: Dijkstra's point, one level up.

So I don't think testing matters *less* than either reading suggests. It matters for a different reason than "proving the code correct". Its job is to make change cheap and regressions loud. The regression tests for `'ï'`, `'x-y'`, and `'℠'` guarantee those bugs can't come back unnoticed, a promise testing can keep. The job of being *sure* belongs to reasoning about the structure of the code, which Dijkstra wanted programmers to do from the start. And the job of *finding* what nobody thought of belongs to generic, unaimed input like `st.text()`. For a search engine whose failures are silent (a missing result looks just like no result), I would rather have all three working together than trust any single one.

---

## Submission

The written reflection is submitted separately from your artifact:

1. Write your responses in this document (or a copy of it, in any editor you like).
2. Upload the completed `WRITTEN.md` to the **HW3 Written** assignment on Gradescope.

### Formatting Guidelines

- **For all parts:** Aim for and prioritize clarity and honest engagement.
- **Part 1**: ~1–2 paragraphs each
- **Part 2**: **~500–700 words** (roughly one single-spaced page). It's fine to go slightly over.

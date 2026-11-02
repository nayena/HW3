# HW3 Grading Rubric

This assignment is evaluated using **two independent letter grades**, as described in the syllabus:

* **Artifact & Automation Grade:** evaluates your technical work and your engagement with the tools
* **Written Reflection Grade:** evaluates your theory-building, reflection, and engagement with course ideas

These two grades measure *different learning outcomes*. They are not averaged mechanically, and strong performance in one does not automatically imply strong performance in the other.

---

## Part A: Artifact & Automation Grade

This grade evaluates how you engaged with the technical work of testing the search engine, finding its bugs, and checking your own tests.

You are **not** graded solely on whether everything works. You *are* graded on whether your work shows good-faith effort, intentionality, and engagement with the tools.

The Gradescope autograder checks your tests, the grading checks, lint, and your Task 8 kill, but its score is not your letter grade.

### Artifact Grade: A+ / A / A-

You will receive an A-range artifact grade if **most** of the following are true:

* Your new example-based tests (Task 2) each check something specific, and together they cover diacritics, hyphens, and the search results that depend on them
* `check_property` works, including the seed and exceptions (Task 3)
* Your new property states something the provided properties don't (Task 4)
* Your generators produce varied inputs, and your tests use them to find the Task 6 bugs (Task 5)
* Each regression test records the original and the minimized counterexample, and both bugs are fixed in `normalize_query` (Task 6)
* Your Hypothesis tests found the third bug, a regression test records what Hypothesis reported, and the fix keeps the two normalizers consistent (Task 7)
* You judged each mutant that survived your non-Hypothesis tests correctly as a real gap or a change no test could notice, your named kill holds up, and you explained why your Hypothesis tests killed what your other tests missed (Task 8)
* Lint passes, and no provided test, grading check, or property was changed, skipped, or deleted

This grade reflects **strong control over the testing tools and what they tell you**, even if minor gaps remain.

---

### Artifact Grade: B+ / B / B-

You will receive a B-range artifact grade if:

* Most tasks are complete, but some tests are shallow (for example, they only check that a result is not empty)
* The generators pass the grading checks but your tests barely use them
* The bugs are fixed, but the regression tests don't record how their inputs were found or minimized
* The mutant analysis is present but doesn't explain why each mutant survived

This grade reflects **substantial progress**, but with clear room for improvement.

---

### Artifact Grade: C+ / C

You will receive a C-range artifact grade if:

* There is clear evidence of effort and engagement with the assignment
* The early tasks (2–4) are mostly done, but few of the later ones (5–8) are
* The bugs may not all be fixed, but there is evidence that you found them

This grade reflects a **good-faith attempt** that did not fully succeed technically.

---

### Artifact Grade: D / E

You will receive a D or E if:

* There is little evidence of engagement with the technical work
* Tests or grading checks were bypassed, disabled, or removed
* Minimal or superficial changes were made
* The submission does not reflect a serious attempt to complete the assignment

---

## Part B: Written Reflection Grade

This grade evaluates the quality of your reflection, theory-building, and engagement with course readings and ideas.

The written component is not a summary or justification. It is an opportunity to demonstrate *how you understand what you worked on*, including confusion, failure, or disagreement.

---

### Reflection Grade: A+ / A / A-

You will receive an A-range reflection grade if:

* Your writing is specific, honest, and grounded in your actual experience
* You compare your own minimization with Hypothesis's using the actual inputs, and say what each taught you about its bug (Part 1A)
* You use your Task 5 and Task 7 results to show where knowing the domain helped and where it limited you (Part 1B)
* You use your own mutants to show what mutation testing told you that a passing test run couldn't (Part 1C)
* You argue for a position on what the search engine should do, and who should decide, rather than listing both sides (Part 1D)
* Your essay engages analytically with **both** Dijkstra and *Software Engineering at Google*, takes a clear position, and grounds it in your experience (Part 2)
* Frameworks from other course readings are used analytically, not just mentioned

This grade reflects **strong theory-building** or a well-defended critique.

---

### Reflection Grade: B+ / B / B-

You will receive a B-range reflection grade if:

* Your reflection is thoughtful and accurate, but limited in depth or synthesis
* Your essay addresses the prompt, but engages one reading much more than the other, or describes both without taking a position
* Examples from your work are present but underdeveloped

This grade reflects **solid understanding**, with room to go deeper.

---

### Reflection Grade: C+ / C

You will receive a C-range reflection grade if:

* Your reflection is honest but vague or shallow
* You acknowledge confusion or partial understanding without fully unpacking it
* The readings are referenced only in passing, or the essay answers a different question than the one asked
* Some sections are missing

This grade reflects **partial theory-building** and awareness of learning gaps.

---

### Reflection Grade: D / E

You will receive a D or E if:

* The reflection is generic, boilerplate, or disconnected from the assignment
* There is little evidence of genuine engagement or understanding
* AI use (if any) is hidden or uncritically accepted

---

## How to Interpret the Two Grades

You will receive **two separate letter grades** for HW3: one for the artifact and one for the written reflection.

Examples:

* **Artifact: C+, Reflection: A** → strong understanding despite incomplete execution
* **Artifact: A-, Reflection: C** → working tests but shallow engagement
* **Artifact: B, Reflection: B+** → solid performance across both dimensions

Both grades matter. A strong written reflection can partially offset incomplete technical execution, though both are expected to show meaningful effort by this point in the semester.

---

## Final Note

The goal of this assignment is to treat each test as a claim about what "correct" means, and to ask how good that claim is, who made it, and what it can't see.

---

## Notes

* Accurate self-assessment (Part 0) demonstrates the kind of self-awareness we value and is taken into account when calibrating grades at the margins.
* Students may be selected for an **oral exam** to discuss their artifact and reflection.

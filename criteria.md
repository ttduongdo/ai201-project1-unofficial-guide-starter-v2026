# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** A couple of my questions depend on retrieving a specific reply over a similar one in the same thread (e.g. pass/fail reply 2 vs. reply 1), so I expect at least one to be harder than the rest. 4 of 5 tolerates one hard question but missing two would mean retrieval itself is broken.
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** This is formatting behavior so it should not be broken, otherwise the prompt itself is broken.
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:** One pass means noise from the gate's threshold being at the edge for some particular phrasing but more than that means consistent failure.
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

---

## 4. Chunk contains all parts of a compound fact

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

For the meal plantier question ("how many times can you change your meal plan 
tier, and by when?"), the single retrieved chunk contains both the count and 
the deadline together, not split across two chunks in at least 4 of 5
tries.

**Why this target:** The answer to this question lives in one sentence of `thread_meal_plan_tier` reply 3 ("you can only change it once and only in the first ten days"). So a correctly-sized chunk should never need to stitch two chunks together to get both halves. 4 of 5 only because chunk boundaries can shift slightly if the pipeline rechunks between runs, when I'm only watching for is a consistent mid-sentence split.



---

## 5. When a thread has multiple conflicting replies, the system cites the highest-voted reply as its source in at least 4 of 5 tries.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->
The system's cited source is the higher-voted reply, not merely the first reply in the thread or any reply that happens to mention the topic.


**Why this target:** I picked three questions spanning a landslide gap (47/20), a medium gap (38/24), and a close gap (41/33) specifically so this criterion is testing whether ranking holds up as the vote gap narrows. 4 of 5 rather than 5 of 5 because the closest case (41 vs 33) is kind of ambiguous when I'm only watching for consistent failures.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->

# The Unofficial Guide

Robbie - Corpus: advice_threads

---

# Unit 1

## What This Does

This is a Q&A system over the `advice_threads` corpus of 23 forum threads where students give advice about their campus life, dining, dorms, deadlines, clubs, and more. Each thread holds several replies ranked by votes answering a specific question. Ask the corpus about something it covers and it should answer with a source file. If asked something outside of scope, the corpus should state so instead of guessing.
<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:** No fixed size but split on reply boundaries (`--- reply N (X votes) ---`). One reply per chunk, with the thread title prepended to it.
**Overlap:** None. 

Each document in `advice_threads/documents` is a forum thread made of 3–5 replies, each answering the thread's question independently. A fixed character window was the wrong tool for that shape, specifically at 800 characters it barely cut anything (26 chunks from 23 documents, one whole thread per chunk), which buried a specific reply's vote count and content inside other unrelated opinions. That's exactly the problem criterion 5 depends on where I need to cite *the highest-voted reply*.

I started by considering a smaller fixed window of 200–300 characters instead of splitting by replies, which is about the average length of a reply. I dropped it because a fixed window doesn't know where one reply ends and the next begins. This strategy encounters the same behavior as the fallback chunker where we have a 2-character trailing fragment from a document. Splitting on the actual `--- reply ---` marker instead means every chunk boundary is a real structural boundary in the document so there was no fragment problem to solve with overlap in the first place.

I also prepend the thread title to every reply chunk, because a reply alone often does not restate what it's answering. Without the title, a chunk could match a question by vocabulary but fail the "could someone answer a question using only this" test.

Result: 75 chunks, averaging 174 characters (shortest 104, longest 253) - up from 26 chunks averaging 487 characters under the fixed-window fallback. No chunk is a whole thread anymore, and the shortest chunk went from a 2-character fragment to 104 characters.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `python app.py --corpus advice_threads chunks -n 1`

```
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.

--- reply 3 (22 votes) ---
Both true. I keep a cheap bike for September to November and walk the rest of the year. Total cost was about $120 for the bike and I don't care what happens to it.

--- reply 4 (5 votes) ---
If you do get one, the campus does free registration and it's the only reason I got mine back after it was taken.
```

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `python app.py --corpus advice_threads chunks -n 5`

```
THREAD: Is a bike worth it for a 20 minute walk commute?
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.
```

**Chunk 2** — source: `thread_first_gen.txt#1 ` — produced by: `python app.py --corpus advice_threads chunks -n 5`

```
THREAD: Anything specific for first-generation students?
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.
```

**Chunk 3** — source: `thread_laptop_specs.txt#2` — produced by: `python app.py --corpus advice_threads chunks -n 5`

```
THREAD: How much laptop do I actually need for CS courses?
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.
```

**Chunk 4** — source: `source: thread_parking.txt#1` — produced by: `python app.py --corpus advice_threads chunks -n 5`

```
THREAD: Worth getting a parking permit?
Street parking on Verrill is legal and free and unmarked, which is why half the upper years do it.
```

**Chunk 5** — source: `thread_sleep_schedule.txt#1` — produced by: `python app.py --corpus advice_threads chunks -n 5`


```
THREAD: Everyone says fix your sleep. Does it actually matter?
The library being open until 2am is a trap. It's a resource, not a schedule.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** How many times can you change your meal plan tier, and by when?

**Answer:** 

```
  (best distance 0.161, cutoff 0.6)

According to thread_meal_plan_tier.txt, you can change your meal plan tier only once and only in the first ten days.

Sources retrieved: thread_meal_plan_tier.txt, thread_pass_fail.txt
```

**My relevance cutoff:** 0.6, unchanged from the default. My in-scope questions landed between 0.1-0.4 and out-of-scope landed between 0.8-0.9 so that's a clean cutoff. Near-miss questions landed at 0.2-0.3 which is inside the in-scope range since the topic is covered but the exact answers are not mentioned.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance | Category |
|---|---|---|---|
| How many times can you change your meal plan tier, and by when? | yes | 0.161 | in scope |
| According to students, what's the best time to ask an instructor for a late-deadline extension? | yes | 0.404 | in scope |
| When should you use the pass/fail option, and how late can you declare it? | yes | 0.211 | in scope |
| What's the one thing first-generation students are told to ask about explicitly? | yes | 0.371 | in scope |
| When is laundry least busy in the dorms? | yes | 0.206 | in scope |
| What is the capital of Mongolia? | no | 0.899 | out of scope |
| How do I change the oil in a diesel engine? | no | 0.905 | out of scope |
| Who won the 1994 World Cup? | no | 0.898 | out of scope |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.819 | out of scope |
| How do I write a for loop in Rust? | no | 0.861 | out of scope |
| How much does a parking permit cost? | no | 0.340 | near miss |
| What's the price per page for color printing? | no | 0.251 | near miss |
| Is there a fee to change your meal plan tier? | no | 0.297 | near miss |
| Do transfer credits count toward financial aid? | no | 0.374 | near miss |
| Which library study room has the best wifi? | no | 0.360 | near miss |
## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I asked Claude on the regex to split replies in my chunking strategy and later on to reverse check if a chunk makes sense on its own, which Claude added prepending the title.

**2.** After running "best time to ask for a late-deadline extension", the answer cited both `thread_late_work.txt` and `thread_group_project.txt`, but those two threads are about different situations (an instructor extension vs. a disappearing group member) that just happen to share similar phrasing. Claude pointed out a new near-miss, meaning the model was blending two documents' claims into one sentence. The suggested fix was to add a line to `GROUNDING_INSTRUCTION` telling the model not to merge similar claims from different documents unless they're actually about the same situation.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->
## Stretch features
### Metadata filtering
**Motivation:** Each chunk carries a vote count of the reply it came from. Store as `votes` in Chroma metadata and make `retrieve` accept a `--min-votes N` argument, which filters chunks below a vote count threshold before ranking.

**Question:** "How many times can you change your meal plan tier, and by when?"

**No filtering** — produced by: `python app.py --corpus advice_threads retrieve "How many times can you change your meal plan tier, and by when?"`

| # | distance | source | votes |
|---|---|---|---|
| 1 | 0.1611 | thread_meal_plan_tier.txt | 11 |
| 2 | 0.3109 | thread_meal_plan_tier.txt | 19 |
| 3 | 0.3731 | thread_meal_plan_tier.txt | 24 |
| 4 | 0.3845 | thread_meal_plan_tier.txt | 7 |
| 5 | 0.7153 | thread_pass_fail.txt | — |

**With filtering** — produced by: `python app.py --corpus advice_threads retrieve "How many times can you change your meal plan tier, and by when?" --min-votes 15`

| # | distance | source | votes |
|---|---|---|---|
| 1 | 0.311 | thread_meal_plan_tier.txt | 19 |
| 2 | 0.373 | thread_meal_plan_tier.txt | 24 |
| ... | | | |

**What changed:** The correct and most relevant answer with distance 0.161 ("you can only change it once, in the first ten days") has only 11 votes. Filtering at `--min-votes 15` removes it and promotes less relevant replies in the same thread to the top instead.

This means vote-based filtering is a poor default for this corpus, since vote count measures agreement with a reply within its own thread, not relevance to an arbitrary question being asked of the corpus. A factual reply to the question might ending up being a lesser-upvoted reply in its thread.

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

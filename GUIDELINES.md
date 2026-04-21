# Guidelines — Lëtzebuergesch Tools

Every time you work on this project, follow this checklist. No exceptions.

## Before Starting Work

- [ ] Read this file
- [ ] Read `docs/research.md` for current state of Luxembourgish NLP
- [ ] Read `docs/PLAN.md` for project phases

## After Making Changes

- [ ] Update `README.md` if project description, status, or feature list changed
- [ ] Update `CONTRIBUTING.md` if setup instructions or dependencies changed
- [ ] Update `SECURITY.md` if attack surface changed
- [ ] Update `docs/PLAN.md` if milestones or phase scope changed
- [ ] Update `docs/research.md` if new resources or gaps discovered
- [ ] Update the landing page at `ltz.joelclaw.lu` if "What Exists" or "What's Missing" sections changed
- [ ] Update the projects page on `joelclaw.lu/projects/` if project description changed
- [ ] Update the homepage on `joelclaw.lu` if project card needs updating
- [ ] Update the About page stats on `joelclaw.lu/about/` if project count changed
- [ ] Git commit AND push to GitHub
- [ ] Verify the deployment on ltz.joelclaw.lu (curl for 200)

## Blog Posts About This Project

- [ ] Never use real last names (blog rule)
- [ ] Cite sources for every factual claim
- [ ] No em dashes — use commas or parentheses instead
- [ ] Use apostrophe for thousands separator (10'000 not 10,000)
- [ ] Cross-post link to the project repo and website

## Sproochentest Reference

The Sproochentest is the Luxembourgish language proficiency exam required for citizenship (naturalization). It's administered by INLL (Institut National des Langues / Nationalinstitut fir Sproochen).

### Structure

**Two compulsory tests, no written component:**

#### 1. Oral Expression (Speaking) — Level A2

**What's tested:**
- Introduce yourself and speak about familiar topics in simple terms
- Describe and compare people, things, and activities
- Answer questions on everyday topics

**Topics (candidate chooses from a list):**
- Work / Occupation
- Education / Training
- Family
- Friends
- Hobbies / Leisure
- Food and Drink
- Media
- Travel / Holidays
- Languages
- Health
- Home / Living conditions

**Format:**
- Part 1: Interview with examiner on chosen topic (5 minutes)
  - Examiner offers 2 topics, candidate picks 1
  - Examiner may ask follow-up questions (can be tricky/leading)
- Part 2: Description of a visual medium (5 minutes)
  - Candidate picks 1 of 3 photos or drawings
  - Must describe what they see
  - **Key grammar:** Dative case is critical for picture description
  - Must answer "where" questions correctly (on the table, by the bed, etc.)
  - Prepositions with dative articles are heavily tested

**Evaluation criteria (8 dimensions):**
1. Vocabulary repertoire
2. Use of basic grammatical structures
3. Fluency
4. Clarity
5. Task fulfilment
6. Coherence
7. Ability to make oneself understood
8. Interaction

**Duration:** 10 minutes (2 × 5)

#### 2. Listening Comprehension — Level B1

**What's tested:**
- Understand main points of clear standard speech on familiar matters
- Deal with most situations while travelling in Luxembourgish-speaking areas
- Understand radio/TV programs on current topics (when delivery is slow and clear)

**Format: 3 listening exercises:**
1. Radio news item (e.g., kangaroo escaped from zoo, car accident, police report)
2. Everyday conversation between two people
3. Discussion or presentation on a specific topic (interview format)

**Each exercise:**
- Audio played twice
- 3-7 multiple-choice questions per exercise
- Mark answers on answer sheet
- Can be done on iPad or with group

**Duration:** ~25 minutes total (plus 10 min speaking in same session)

### Passing Criteria

- Must score **at least 50% on the speaking test** to pass
- If speaking is below 50%, listening can compensate IF the **average of both tests is ≥ 50%**
- Listening alone cannot compensate — you cannot pass with a poor speaking score
- **Speaking is more important than listening** in the scoring
- Total possible: 100 points per section
- Cost: ~€75

### Critical Pitfalls

1. **Don't switch to German** — examiners don't like it. If you forget a Luxembourgish word, use French or English instead
2. **Don't go silent** — long silences are recorded and reduce your score significantly
3. **Don't over-embellish** — stick to the topic, don't tell elaborate stories
4. **Don't criticize Luxembourg** — examiners are human, negative attitudes affect scoring
5. **Dative case is essential** — picture description requires spatial prepositions with correct articles
6. **Cheating = 1 year ban** — don't copy, photograph, or share exam content

### What This Means for Lëtzebuergesch Tools

The Sproochentest is a key use case. Our tools should help people prepare:

1. **Grammar checker** must catch dative case errors (the #1 grammar point tested)
2. **Readability scorer** should align with A2/B1 CEFR levels
3. **Graded word lists** should cover the Sproochentest topic vocabulary
4. **Writing assistant** should help with spatial descriptions (dative prepositions)
5. **Practice mode** could generate picture descriptions and evaluate them
6. **Listening practice** could use Schreifmaschinn TTS to generate exercises
7. **Topic vocabulary** should be organized by Sproochentest categories (work, family, food, etc.)

### Sources

- INLL official: https://www.inll.lu/en/sproochentest-en/
- Sproochentest.org: https://sproochentest.org/what-is-the-sproochentest/
- Learn Easy Luxembourgish: https://www.learneasyluxembourgish.com/en/blog-posts/what-is-included-in-sproochentest.html
- Luxtoday interview: https://luxtoday.lu/en/interview/learning-a-language/what-is-the-sproochentest-and-how-to-pass-it

## Research Resources

Key contacts for collaboration:
- **ZLS** (Zenter fir d'Lëtzebuerger Sprooch) — official language authority, owns spellchecker.lu since 2023, maintains Schreifmaschinn and LOD
- **Michel Weimerskirch** — spellchecker.lu creator (2006), transferred to ZLS in 2023
- **Alistair Plum** (Uni.lu) — LuxBank, text normalization
- **Julian Valline, Cédric Lothritz, Jordi Cabot** (LIST) — LuxIT instruction tuning dataset
- **Fred Philippy, Laura Bernardy** (SnT, Uni.lu) — LuxInstruct cross-lingual dataset

Key datasets and tools:
- spellchecker.lu — HunSpell dictionary (ZLS-owned, CC0 release pending)
- LOD (lod.lu) — official multilingual dictionary with API
- Schreifmaschinn.lu — STT (Whisper) and TTS (VITS2)
- LuxBank — first UD treebank for Luxembourgish
- spellux — text normalization (MIT license)
- LuxemBERT — BERT model for Luxembourgish
- LuxIT — 59'242 monolingual instruction tuning pairs
- LuxInstruct — cross-lingual instruction tuning dataset
- LUXMT — GEMMA 3 27B fine-tuned for LB→FR/EN translation
- Grammar-Book-Guided Probing — systematic LLM grammar evaluation
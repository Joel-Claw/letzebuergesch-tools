# Luxembourgish Language Technology & Education Research

## For: Language tools project (current) + future project (TBD)
## Date: 2026-04-21

---

## Existing Language Technology

### ZLS (Zenter fir d'Lëtzebuerger Sprooch)
- **Website:** https://www.zls.lu
- **Twitter:** @den_ZLS
- **Role:** Government language center, official authority on Luxembourgish orthography and rules
- **BEST RESOURCE for orthography rules and standardization**
- **HuggingFace orgs:**
  - denZLS (3 models): luxembourgish-male-vits-tts (TTS)
  - ZLSCompLing (5 models, 3 datasets)
- **ZLSCompLing models:**
  - Whisper-Large-V3-Turbo-Luxembourgish-fp16 (ASR, updated 6 days ago, 25 downloads)
  - Whisper-Large-V3-Turbo-Luxembourgish (ASR)
  - VITS2-Claude (TTS, gender-neutral voice)
  - CoquiTTS-Maxine (TTS)
  - CoquiTTS-Max (TTS)
- **ZLSCompLing datasets:**
  - LOD_Claude (39k entries)
  - LOD_Maxine (32k entries)
  - validator_38h (23.8k entries)
- **Key product: Sproochmaschinn.lu** (launched Feb 10, 2025)
  - Schreifmaschinn: speech-to-text (Whisper-based), improved regional dialect coverage, longer recordings, timestamps for video subtitling
  - Liesmaschinn: text-to-speech (VITS2), voice of Max Kuborn (RTL), trained on LOD data
  - Data privacy: no text/audio stored after processing
  - Contact for enterprise use: lod@lod.lu
  - Explicitly recommends spellchecker.lu for orthography checking
  - Limitations: struggles with foreign loanwords, proper nouns (places, people, institutions), abbreviations
  - TTS works best with correctly spelled text

### spellchecker.lu
- **Website:** https://spellchecker.lu (online checker)
- **Dictionary API:** https://dictionary.spellchecker.lu/ (thesaurus + manager)
- **Creator:** Michel Weimerskirch (founded 2006 as private initiative)
- **GitHub:** https://github.com/spellchecker-lu/dictionary-lb-lu (23 stars, 2 forks)
- **What it is:** HunSpell dictionary + MyThes thesaurus for Luxembourgish
- **Thesaurus:** th_lb_LU_v2.idx has 12'804 entries (seen in GitHub)
- **Available as:** online checker, LibreOffice extension, browser extension
- **Status:** TAKEN OVER BY ZLS in 2023. GitHub repo appears stale (Jan 2023) because development moved to ZLS. Relaunched with fresh look for Rentrée 2023.
- **License:** Word list to be released under CC0 (announced Sep 2023, pending final review)
- **1 open issue on GitHub**
- **History:** Founded 2006 by Weimerskirch. 2019: first productive contacts with ZLS for orthography updates. 2023: ZLS officially took over the platform. Completes ZLS tool portfolio alongside LOD and Schreifmaschinn.
- **New app version** announced for end of 2023

### LOD (Lëtzebuerger Online Dictionnaire)
- **Website:** https://www.lod.lu
- **API:** https://api.lod.lu
- **Open Data:** https://data.public.lu/en/datasets/letzebuerger-online-dictionnaire-lod-public-api/
- **Linguistic Data:** https://data.public.lu/en/datasets/letzebuerger-online-dictionnaire-lod-linguistesch-daten/
- **npm package:** lod-opendata (for programmatic access)
- **What it is:** Official multilingual dictionary (Luxembourgish ↔ German, French, Portuguese, English)
- **Backbone dataset for ZLS TTS training**
- **Key resource for any language tooling project**

### Academic NLP Research

#### LuxIT (Oct 2025)
- First monolingual instruction tuning dataset for Luxembourgish
- Authors: Julian Valline, Cédric Lothritz, Jordi Cabot (LIST)
- arXiv: 2510.24434
- 59'242 instruction-answer pairs synthesized from RTL.lu + Wikipedia Luxembourgish articles
- Used DeepSeek-R1-0528 for generation (best Luxembourgish proficiency)
- Quality assurance via LLM-as-judge approach
- Fine-tuning on LuxIT showed mixed results across different models
- **Critical for LLM training efforts**

#### LuxInstruct (Oct 2025)
- First large-scale cross-lingual instruction tuning dataset for Luxembourgish
- Authors: Fred Philippy, Laura Bernardy, Siwen Guo, Jacques Klein, Tegawendé F. Bissyandé (SnT, Uni.lu)
- arXiv: 2510.07074
- HuggingFace: https://huggingface.co/datasets/fredxlpy/LuxInstruct
- **Cross-lingual approach (different from LuxIT's monolingual approach)**
- **Critical for LLM training efforts**

#### LUXMT (Feb 2026)
- Machine translation system based on GEMMA 3 27B
- Fine-tuned for Luxembourgish → French and English translation
- Author: Nils Rehlinger (Uni.lu)
- arXiv: 2602.15506
- **Demonstrates viable LLM fine-tuning for Luxembourgish**

#### LuxBank (Nov 2024)
- First Universal Dependency Treebank for Luxembourgish
- Authors: Alistair Plum, Caroline Döhmer, Emilia Milano (Uni.lu)
- ACL Anthology: https://aclanthology.org/2024.tlt-1.4/
- arXiv: 2411.04813
- **Critical for POS tagging and dependency parsing**

#### Neural Text Normalization (Dec 2024)
- Authors: Anne-Marie Lutgen, Alistair Plum, Christoph Purschke, Barbara Plank (Uni.lu + LMU Munich)
- arXiv: 2412.09383
- **Normalizes variant Luxembourgish spellings to standard form**
- Uses real-life variation data
- **Directly applicable to education tools**

#### spellux (2020, MIT license)
- GitHub: https://github.com/questoph/spellux (12 stars, 5 forks)
- Automatic text normalization for Luxembourgish
- Python-based
- **Could be foundation for teacher-facing normalization tools**

#### LuxemBERT (2022)
- Uni.lu research
- BERT model pre-trained for Luxembourgish with data augmentation
- ORBilu: https://orbilu.uni.lu/handle/10993/51815
- **Foundation model for NLP tasks**

#### Grammar-Book-Guided Probing (Oct 2025)
- Authors tested LLM grammatical understanding of Luxembourgish
- arXiv: 2510.24856v2
- Code: https://github.com/DobricLilujun/GBGP.git
- **Key finding:** LLMs have weak grammatical understanding of Luxembourgish, especially morphology and syntax. Strong translation ≠ deep grammatical competence. Larger models struggle with minimal pair tasks.
- **Implication:** Can't rely on LLMs alone for grammar checking, need rule-based + ML hybrid

#### Luxembourgish in spaCy
- Added to spaCy NLP tools (Nov 2019)
- https://infolux.uni.lu/letzebuergesch-lo-als-sprooch-an-de-spacy-nlp-tools/
- **Tokenization + POS tagging available but not production-grade for education**

#### Sentiment Analysis for Luxembourgish (2024)
- LUHME workshop paper
- ACL Anthology: 2024.luhme-1.3
- Authors: Hosseini-Kivanani, Kühn, Schommer
- **Low-resource sentiment analysis research**

#### Multilingual ECEC Research
- Claudine Kirsch et al. (Uni.lu): professional development for multilingual early childhood education
- ORBilu: https://orbilu.uni.lu/handle/10993/42529
- DCU presentation (Oct 2024): Towards Multilingual Education in ECEC in Luxembourg
- **Teacher training research, directly relevant to education tools**

---

## Projet Alpha (zesumme wuessen) - Full Context

### What It Is
- Education reform allowing French OR German as literacy language in Cycle 1.2
- Pilot since Sept 2022 in 4 schools (Differdange, Dudelange, Schifflange, Larochette)
- Nationwide rollout: Cycle 1.2 orientation starts 2026/27, formal literacy in Cycle 2.1 from 2027/28

### Key Statistic
- 68% of pupils starting school in 2022-23 came from households where Luxembourgish was NOT the primary language (ministry figure)

### Positive Evidence
- **LUCET first evaluation (June 21, 2024):** Pilot "potentially could contribute to reducing educational inequalities at the beginning of school career"
- RTL Infos: "Le projet pilote Alpha porte ses fruits" (bears fruit)
- Education Minister Claude Meisch: gradual approach built broad support, method works in real classrooms
- Marc Schmit (Centre de Logopédie): matching literacy instruction with spoken language skills reduces complexity of learning to read/write
- International public schools already offered French literacy for nearly a decade

### Criticism & Concerns

#### Teachers
- Not fully confident in guiding families through the new system
- Concern parents may disregard professional guidance when choosing literacy track (parents have final say)
- Sadness over gradual disappearance of traditional preschool model
- Growing number of new projects/expectations pushing creative play into background

#### SNE Union (April 2026, latest)
- Patrick Remakel: "We need all resources at the child"
- Criticizes redistribution of specialized teaching staff (I-EBS/A-EBS) making it more complicated
- New "comités locaux" meeting twice monthly = "administrative waterfall" (lost time)
- Demands resource analysis: who works with the child, who doesn't? Can't waste resources not working with children
- C1 needs one enseignant + one éducateur per class, every day, currently not the case

#### SEW/OGBL Union
- Warns of overloading the school system
- Criticizes missing resources, hierarchy problems, too many reforms at once

#### Parliamentary Criticism
- Ricardo Marques (CSV, government majority!): "A good idea is not yet well implemented"
- Doubts about logistical feasibility
- Concerns about acute staff shortages
- Small municipalities face logistical challenges

#### Children's Ombudsman
- Charel Schmit: "We have to ask ourselves the honest question of how much multilingualism we really need and at what level... and what price it comes at"
- "Trilingualism, which is not something our pupils are born with, is the academic undoing of many"

#### Structural Criticism (Journal.lu)
- Languages are the "big filter" in Luxembourg's school system
- Many pupils cram history, biology and maths with one eye on the dictionary
- Even if French literacy succeeds, it's "a first step from which further learning can take place"
- Secondary school stats: 36% Luxembourgish first language, 26% Portuguese, 12% French, 15% "other"
- 111'485 children in primary+secondary schools (2022/23)

#### Weth (Linguist)
- French orthography less transparent than German
- Transfer problem when French-first then German later
- Luxembourgish literacy would be consistent with C1 preparation but lacks standardized writing norms enforced through school

#### Engel de Abreu (Psychologist)
- Any language works for literacy given sufficient proficiency
- The issue is structural conditions, not the language choice itself

---

## Identified Gaps (What's Missing)

### For LLMs Learning Luxembourgish
1. **No standardized training data pipeline** - LuxIT and LuxInstruct exist but are research artifacts, not production pipelines
2. **Fine-tuning results are mixed** - LuxIT showed varying performance across models, no clear recipe yet
3. **Grammar understanding is weak** - Grammar-Book-Guided Probing (Oct 2025) showed LLMs struggle with morphology and syntax, especially minimal pairs
4. **No benchmark suite** - no standardized way to evaluate LLM Luxembourgish proficiency (LuxIT used language proficiency exams, ad hoc)
5. **Training data is news/Wikipedia-heavy** - Luxembourgish in education, daily life, and creative writing is underrepresented
6. **No orthography-grounded training** - ZLS orthography rules not systematically included in training data

### For Luxembourgish as Written Language
1. **No real grammar checker** - spellchecker.lu only does orthography (HunSpell), not syntax/agreement
2. **No readability scorer** - no way for teachers to assess if text is appropriate for Cycle 1.2 vs Cycle 4
3. **No graded word lists** - no vocabulary lists aligned with school cycles
4. **spellchecker.lu GitHub stale** - development moved to ZLS (takeover 2023), word list CC0 release pending
5. **No educational integration layer** - ZLS tools exist but aren't packaged for classroom use
6. **TTS depends on correct spelling** - Liesmaschinn explicitly says results improve with correct orthography
7. **LLM grammar understanding is weak** - can't rely on LLMs alone for grammar checking (need rule-based + ML hybrid)
8. **No writing support for Luxembourgish** - tools exist for checking but not for helping people write correctly in the first place

### For Teachers
1. **No tools to help them guide parents** through literacy track orientation
2. **No classroom materials** that bridge existing tech (spellchecker, LOD) into usable lesson aids
3. **No text normalization tools** deployed for classroom use (research exists, not deployed)
4. **Resource allocation is opaque** - SNE complaints about "who works with the child"

### For Students
1. **No interactive writing practice** with real-time Luxembourgish orthography feedback
2. **No age-appropriate reading materials** with difficulty indicators
3. **No vocabulary building tools** aligned with curriculum

---

## Fake/Inadequate Tools Found
- **Linguix.com** "Luxembourgish Grammar Checker" - likely just generic wrapper, not Luxembourgish-specific
- **textgens.com** "Luxembourgish Grammar Checker" - generic LLM wrapper, no real Luxembourgish grammar engine
- These are not real Luxembourgish grammar tools

---

## Key People & Institutions
- **ZLS** - official language authority, best orthography reference, now owns spellchecker.lu
- **Michel Weimerskirch** - spellchecker.lu creator (2006), platform transferred to ZLS in 2023
- **Alistair Plum** (Uni.lu) - LuxBank, text normalization, core NLP researcher
- **Anne-Marie Lutgen** (Uni.lu) - text normalization
- **Christoph Purschke** (Uni.lu) - linguistics, text normalization
- **Barbara Plank** (LMU Munich / Uni.lu) - NLP, text normalization
- **Claudine Kirsch** (Uni.lu) - multilingual ECEC, teacher professional development
- **Julian Valline, Cédric Lothritz, Jordi Cabot** (LIST) - LuxIT instruction tuning dataset
- **Fred Philippy, Laura Bernardy** (SnT, Uni.lu) - LuxInstruct cross-lingual instruction tuning
- **Nils Rehlinger** (Uni.lu) - LUXMT translation system
- **Marc Schmit** - Centre de Logopédie, speech therapy perspective on literacy
- **Charel Schmit** - Ombudsman for children and young people
- **Patrick Remakel** - SNE union president
- **Claude Meisch** - Education Minister (DP)
- **Eric Thill** - Culture Minister, presented Sproochmaschinn.lu

## Demographics (STATEC 2021 Census)
- Luxembourgish as main language: 48.9% (down from 55.8%)
- German regular speakers: 23% (down from 31%)
- 68% of school starters don't speak Luxembourgish at home
- Secondary: 36% Luxembourgish first language, 26% Portuguese, 12% French, 15% other
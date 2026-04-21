# Lëtzebuergesch Tools - Project Plan

## Purpose

Lëtzebuergesch Tools exists to build what's missing: a grammar checker, a readability scorer, and graded word lists for Luxembourgish. These tools don't exist yet. Nobody is building them. We are.

Existing tools (ZLS speech-to-text, spellchecker.lu orthography, LOD dictionary) do their jobs well. We're not here to replace them. We're here to fill the gaps they don't cover: grammar, readability, and educational alignment.

## Phase 0: Research (Current)
- [x] Map existing Luxembourgish language technology
- [x] Document Projet Alpha context (positive + negative criticism)
- [x] Identify gaps in tooling for education
- [x] Identify academic research that could be applied
- [ ] Contact ZLS about orthography rules availability (machine-readable format?)
- [ ] Contact Alistair Plum (Uni.lu) about LuxBank/spellux

## Phase 1: Foundation Tools
- [ ] **Grammar checker** - rule-based syntax and agreement checking using ZLS orthography rules. Not LLM-dependent. Catches dative case errors, verb conjugation, article agreement.
- [ ] **Readability scorer** - assess Luxembourgish text difficulty aligned with CEFR levels (A2 through B2) and school cycles.
- [ ] **Graded word lists** - word lists aligned with the 4 fundamental education cycles (C1: ages 3-5, C2: ages 6-7, C3: ages 8-9, C4: ages 10-11). Needs teacher input.
- [ ] **Text normalization** - variant to standard Luxembourgish normalization (build on spellux/Lutgen et al. research)
- [ ] **API and web interface** - all tools accessible via API and a simple web UI

## Phase 2: Education Tools
- [ ] **Teacher dashboard** - single interface for classroom use, no logins or API keys required
- [ ] **Writing assistant** - real-time orthography + grammar feedback while writing
- [ ] **Sproochentest practice** - listening exercises using TTS, picture description evaluation, vocabulary by topic category
- [ ] **Error corpus** - collect common Luxembourgish writing errors with corrections, sourced from teachers

## Phase 3: Community & LLM Support
- [ ] **Teacher feedback loop** - let teachers submit errors they see in student work
- [ ] **Orthography-grounded training data** - incorporate ZLS rules into instruction tuning datasets
- [ ] **Benchmark suite** - standardized evaluation for LLM Luxembourgish proficiency
- [ ] **Grammar evaluation pipeline** - build on Grammar-Book-Guided Probing (arXiv: 2510.24856)

## Design Principles

1. **Honest tools** - if a feature doesn't work well, say so, don't fake it
2. **Build, don't integrate** - we're building new tools, not wrapping existing ones. If ZLS tools had APIs we could use, we'd link to them. They don't, so we build from scratch.
3. **Teacher-first** - tools must solve real classroom problems, not theoretical ones
4. **Local when possible** - text processing should happen on-device, not require cloud
5. **Open data** - word lists, error corpora, and rules should be freely available
6. **Rule-based + ML hybrid** - LLMs alone fail at Luxembourgish grammar; combine rule-based with ML where appropriate
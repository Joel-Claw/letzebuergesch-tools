# Lëtzebuergesch Tools - Project Plan

## Phase 0: Research (Current)
- [x] Map existing Luxembourgish language technology
- [x] Document Projet Alpha context (positive + negative criticism)
- [x] Identify gaps in tooling for education
- [x] Identify academic research that could be applied
- [ ] Contact ZLS about orthography rules availability (machine-readable format?)
- [ ] Contact spellchecker.lu (Michel Weimerskirch) about project collaboration
- [ ] Contact Alistair Plum (Uni.lu) about LuxBank/spellux integration

## Phase 1: Foundation Tools
- [ ] **Orthography API wrapper** - wrap spellchecker.lu HunSpell dictionary + ZLS orthography rules into a clean API
- [ ] **LOD integration** - programmatic access to LOD for definitions, translations, examples
- [ ] **Text normalization** - deploy spellux or build on Lutgen et al. research for variant → standard normalization
- [ ] **Graded word lists** - compile word lists aligned with school cycles (needs teacher input)

## Phase 2: Education Tools
- [ ] **Readability scorer** - assess Luxembourgish text difficulty (which school cycle?)
- [ ] **Grammar checker prototype** - rule-based syntax/agreement checking using ZLS rules (not LLM-dependent)
- [ ] **Teacher dashboard** - integrate all tools into a single interface for classroom use
- [ ] **Writing assistant** - real-time orthography + grammar feedback while writing

## Phase 3: Community
- [ ] **Error corpus** - collect common Luxembourgish writing errors with corrections
- [ ] **Teacher feedback integration** - let teachers submit errors they see in student work
- [ ] **Collaboration with ZLS** - ensure tools align with official standards
- [ ] **Multi-language support** - French + German literacy track tools (Projet Alpha context)

## Phase 4: LLM Training Support
- [ ] **Orthography-grounded training data** - incorporate ZLS rules into instruction tuning datasets
- [ ] **Benchmark suite** - standardized evaluation for LLM Luxembourgish proficiency
- [ ] **Curated training corpus** - go beyond news/Wikipedia to include education, daily life, creative writing
- [ ] **Fine-tuning recipes** - documented approaches for adapting LLMs to Luxembourgish (building on LuxIT/LuxInstruct findings)
- [ ] **Grammar evaluation pipeline** - build on Grammar-Book-Guided Probing (arXiv: 2510.24856) to systematically test and improve LLM grammar understanding

## Design Principles

1. **Honest tools** - if a feature doesn't work well, say so, don't fake it
2. **Integration over reinvention** - use LOD, spellchecker.lu, ZLS tools, don't replace them
3. **Teacher-first** - tools must solve real classroom problems, not theoretical ones
4. **Local when possible** - text processing should happen on-device, not require cloud
5. **Open data** - word lists, error corpora, and rules should be freely available
6. **Rule-based + ML hybrid** - LLMs alone fail at Luxembourgish grammar; combine rule-based with ML where appropriate
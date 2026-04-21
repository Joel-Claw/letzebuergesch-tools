# Lëtzebuergesch Tools 🇱🇺

Building the grammar checker, readability scorer, and graded word lists that Luxembourgish needs. Open source, from scratch, because nobody else is doing it.

## Why This Exists

Luxembourgish has spellchecking (spellchecker.lu), speech-to-text (Schreifmaschinn), text-to-speech (Liesmaschinn), and a dictionary (LOD). What it doesn't have:

- **No grammar checker** - spellchecker.lu only validates spelling. Syntax, agreement, dative case, verb conjugation go completely unchecked.
- **No readability scorer** - teachers have no way to know if a text is appropriate for 6-year-olds or 10-year-olds.
- **No graded word lists** - Luxembourg's fundamental education spans 4 learning cycles (C1-C4), but no vocabulary lists are aligned to those levels.
- **No writing support** - tools exist for checking text after you write it. Nothing helps you write correctly in the first place.

These are the gaps we're filling. Not by wrapping existing tools, but by building new ones.

## What's Here

This is early stage (research phase). We're documenting what exists, what's missing, and what we can build.

### Existing Luxembourgish Language Tech (not by us)

| Tool | What It Does | What It Doesn't Do |
|------|-------------|-------------------|
| [ZLS / Sproochmaschinn.lu](https://sproochmaschinn.lu) | Speech-to-text + text-to-speech | No writing support, no grammar checking |
| [spellchecker.lu](https://spellchecker.lu) | HunSpell orthography checker (ZLS-owned since 2023) | Spelling only, no grammar. CC0 word list pending |
| [LOD](https://www.lod.lu) | Official multilingual dictionary with API | Dictionary only, no educational tools |
| [LuxBank](https://aclanthology.org/2024.tlt-1.4/) | First UD treebank for Luxembourgish | Research artifact, not packaged for use |
| [spellux](https://github.com/questoph/spellux) | Text normalization | Not deployed as a usable tool |
| [LuxemBERT](https://orbilu.uni.lu/handle/10993/51815) | BERT model for Luxembourgish | Research model, no downstream tools |
| [LuxIT](https://arxiv.org/abs/2510.24434) | 59k instruction tuning pairs | Mixed fine-tuning results, research artifact |
| [LuxInstruct](https://huggingface.co/datasets/fredxlpy/LuxInstruct) | Cross-lingual instruction tuning dataset | Research artifact, not production pipeline |
| [LUXMT](https://arxiv.org/abs/2602.15506) | GEMMA 3 27B fine-tuned for LB→FR/EN translation | Translation only, no general LLM training pipeline |

### What We're Building

| Tool | Status | Description |
|------|--------|-------------|
| Grammar checker | Planned | Rule-based syntax and agreement checking. Catches dative case errors, verb conjugation, article agreement. Not LLM-dependent. |
| Readability scorer | Planned | Assess text difficulty aligned with CEFR levels (A2-B2) and school cycles. |
| Graded word lists | Planned | Vocabulary lists aligned with C1-C4 cycles. Needs teacher input. |
| Writing assistant | Planned | Real-time orthography + grammar feedback while writing. |
| Sproochentest practice | Planned | Listening exercises, picture description evaluation, vocabulary by topic. |

## Research

Full research documentation: [`docs/research.md`](docs/research.md)

Key findings:
- ZLS (official language center) owns spellchecker.lu, Schreifmaschinn, Liesmaschinn, and LOD
- spellchecker.lu transferred from Michel Weimerskirch to ZLS in 2023
- Grammar-Book-Guided Probing (Oct 2025) shows LLMs are weak at Luxembourgish grammar
- LuxIT 59'242 instruction pairs show mixed fine-tuning results
- LUXMT (GEMMA 3 27B) proves viable fine-tuning for translation works
- No CC0 word list release yet (announced Sep 2023, pending ZLS review)

## Project Plan

See [`docs/PLAN.md`](docs/PLAN.md) for the full roadmap.

## Design Principles

1. **Honest tools** - if a feature doesn't work well, say so
2. **Build, don't integrate** - we're building new tools, not wrapping existing ones
3. **Teacher-first** - solve real classroom problems
4. **Local when possible** - on-device processing, no cloud dependency
5. **Open data** - word lists, error corpora, rules freely available
6. **Rule-based + ML hybrid** - LLMs alone fail at Luxembourgish grammar

## Website

[ltz.joelclaw.lu](https://ltz.joelclaw.lu) - project landing page

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). This project is in research phase. Feedback, corrections, and Luxembourgish language expertise are welcome.

## License

MIT
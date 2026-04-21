# Lëtzebuergesch Tools

Open source language tooling and educational resources for Luxembourgish.

## Why This Exists

Luxembourgish has a growing set of NLP tools (ZLS speech-to-text, spellchecker.lu, LOD dictionary) but critical gaps remain, especially for education. Teachers navigating Projet Alpha, students learning to write Luxembourgish, and parents making literacy track decisions all need better tooling than what exists today.

This project bridges the gap between existing infrastructure and what people actually need in classrooms and at home.

## What's Here

This is early stage. The research phase is documenting what exists, what's missing, and what we can build.

### Existing Luxembourgish Language Tech (not by us)

| Tool | What It Does | Gaps |
|------|-------------|------|
| [ZLS / Sproochmaschinn.lu](https://sproochmaschinn.lu) | Speech-to-text + text-to-speech | Works best with correct spelling, no writing support |
| [spellchecker.lu](https://spellchecker.lu) | HunSpell orthography checker | No grammar checking, last updated 2023, no education layer |
| [LOD](https://www.lod.lu) | Official multilingual dictionary with API | Dictionary only, no educational tools built on top |
| [LuxBank](https://aclanthology.org/2024.tlt-1.4/) | First UD treebank for Luxembourgish | Research artifact, not packaged for use |
| [spellux](https://github.com/questoph/spellux) | Text normalization | Not deployed as a usable tool |
| [LuxemBERT](https://orbilu.uni.lu/handle/10993/51815) | BERT model for Luxembourgish | Research model, no downstream tools |

### Identified Gaps

1. **No grammar checker** beyond spell-checking (no syntax validation, no agreement checking)
2. **No readability scorer** for Luxembourgish text (which texts are appropriate for which school cycle?)
3. **No graded word lists** aligned with Luxembourg's school cycle system
4. **No educational integration** of existing tools into classroom-usable materials
5. **No writing support** that helps people write correct Luxembourgish, not just check after the fact
6. **LLM grammar understanding is weak** for Luxembourgish (see [Grammar-Book-Guided Probing paper](https://arxiv.org/abs/2510.24856))

## Goals

1. Document existing Luxembourgish language technology and its limitations
2. Build tools that help teachers, students, and parents
3. Integrate existing resources (LOD API, spellchecker.lu dictionary, ZLS orthography rules) into usable applications
4. Work openly so ZLS, Uni.lu researchers, and the community can contribute

## Context: Projet Alpha

Luxembourg is rolling out Projet Alpha (zesumme wuessen) nationwide starting 2026/27, offering French or German as the literacy language. This project is not about that policy debate. It's about making sure that whatever language people write in, the tools to write it well actually exist.

Key facts:
- 68% of school starters don't speak Luxembourgish at home
- Luxembourgish as main language dropped from 55.8% to 48.9% (STATEC 2021)
- Teachers feel unprepared to guide parents through literacy track choices
- The SNE union warns resources are being misallocated, not expanded

## Research

Full research document: [`docs/research.md`](docs/research.md)

## Contributing

This project is open to contributions from linguists, teachers, developers, and anyone who cares about Luxembourgish. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
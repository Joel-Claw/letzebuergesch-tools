"""Tests for common text utilities."""

import pytest
from src.common.text import tokenize, split_sentences, normalize, word_frequency, sentence_stats


class TestTokenize:
    def test_simple_text(self):
        tokens = tokenize("D'Kommereze steet zu Lëtzebuerg.")
        assert len(tokens) >= 4
        assert tokens[0].text == "D'Kommereze"
        assert tokens[0].kind == "word"

    def test_numbers(self):
        tokens = tokenize("Et sinn 42 Schüler.")
        numbers = [t for t in tokens if t.kind == "number"]
        assert len(numbers) == 1
        assert numbers[0].text == "42"

    def test_punctuation(self):
        tokens = tokenize("Wéi geet et? Gutt!")
        puncts = [t for t in tokens if t.kind == "punct"]
        assert len(puncts) == 2

    def test_empty_string(self):
        assert len(tokenize("")) == 0

    def test_luxembourgish_chars(self):
        tokens = tokenize("Lëtzebuerg")
        assert len(tokens) == 1
        assert tokens[0].text == "Lëtzebuerg"


class TestSplitSentences:
    def test_single_sentence(self):
        sentences = split_sentences("D'Kommereze steet zu Lëtzebuerg.")
        assert len(sentences) == 1

    def test_multiple_sentences(self):
        text = "D'Kommereze steet zu Lëtzebuerg. Et ass schéin. Mir ginn heem."
        sentences = split_sentences(text)
        assert len(sentences) == 3

    def test_abbreviation_not_split(self):
        text = "Dat ass z.B. gutt. Dat ass och gutt."
        sentences = split_sentences(text)
        assert len(sentences) == 2

    def test_empty_string(self):
        assert len(split_sentences("")) == 0

    def test_question_mark(self):
        sentences = split_sentences("Wéi geet et? Mir sinn gutt.")
        assert len(sentences) == 2


class TestNormalize:
    def test_lowercase(self):
        assert normalize("Lëtzebuerg") == "lëtzebuerg"

    def test_collapse_whitespace(self):
        assert normalize("ee  zwee   dräi") == "ee zwee dräi"

    def test_apostrophe_normalization(self):
        assert normalize("d'Kommereze") == "d'kommereze"

    def test_strip(self):
        assert normalize("  text  ") == "text"


class TestWordFrequency:
    def test_basic(self):
        freq = word_frequency("Haus Haus Auto")
        assert freq["haus"] == 2
        assert freq["auto"] == 1

    def test_empty(self):
        assert word_frequency("") == {}

    def test_case_insensitive(self):
        freq = word_frequency("Haus haus HAUS")
        assert freq["haus"] == 3


class TestSentenceStats:
    def test_basic_stats(self):
        stats = sentence_stats("D'Kommereze steet zu Lëtzebuerg. Et ass schéin.")
        assert stats["sentence_count"] == 2
        assert stats["word_count"] >= 5
        assert stats["avg_sentence_length"] > 0
        assert stats["type_token_ratio"] > 0

    def test_empty(self):
        stats = sentence_stats("")
        assert stats["sentence_count"] == 0
        assert stats["word_count"] == 0
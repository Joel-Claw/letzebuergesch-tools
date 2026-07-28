"""Tests for the readability scorer."""

import pytest
from src.readability.scorer import ReadabilityScorer


@pytest.fixture
def scorer(wordlist):
    return ReadabilityScorer(wordlist)


class TestReadability:
    def test_empty_text(self, scorer):
        result = scorer.score("")
        assert result.word_count == 0
        assert result.cefr_level == "A1"

    def test_simple_text(self, scorer):
        # Short, simple sentences
        text = "D'Kommereze steet zu Lëtzebuerg. Et ass schéin."
        result = scorer.score(text)
        assert result.word_count > 0
        assert result.sentence_count >= 1
        assert 0 <= result.overall_score <= 100
        assert result.cefr_level in ["A1", "A2", "B1", "B2", "C1", "C2"]

    def test_long_text(self, scorer):
        # Longer, more complex sentence
        text = (
            "D'Regierung vum Groussherzogtum Lëtzebuerg huet eng Rei vun "
            "Projeten am Beräich vun der digitaler Transformatioun ugestart, "
            "déi d'Zil hunn, d'Effizienz vun de ëffentleche Verwaltungen "
            "ze verbesseren an d'Bierger méi einfach Zougank zu de Servicer "
            "ze bidden."
        )
        result = scorer.score(text)
        assert result.word_count > 10
        assert result.avg_sentence_length > 10
        assert result.overall_score < 80  # Should be moderately difficult

    def test_score_text_level(self, scorer):
        level = scorer.score_text_level("D'Kommereze steet zu Lëtzebuerg.")
        assert level in ["A1", "A2", "B1", "B2", "C1", "C2"]

    def test_difficulty_label(self, scorer):
        result = scorer.score("D'Kommereze steet zu Lëtzebuerg.")
        assert result.difficulty_label in [
            "Very easy", "Easy", "Moderate", "Difficult", "Very difficult"
        ]
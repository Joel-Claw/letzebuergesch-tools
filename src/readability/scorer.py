"""Readability scorer for Luxembourgish text.

Scores text difficulty using:
- Word frequency (based on ZLS dictionary rank)
- Sentence length
- proportion of unknown/difficult words
- CEFR level estimation

This is a research-grade tool. Luxembourgish readability has no
established formula (unlike English Flesch-Kincaid), so we use a
composite heuristic approach.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from src.common.text import tokenize, split_sentences, sentence_stats
from src.wordlist.loader import WordList


@dataclass
class ReadabilityScore:
    """Readability assessment for a text."""
    overall_score: float = 0.0  # 0-100, higher = easier
    cefr_level: str = "A1"  # Estimated CEFR level
    word_count: int = 0
    sentence_count: int = 0
    avg_sentence_length: float = 0.0
    unknown_ratio: float = 0.0  # fraction of words not in dictionary
    difficult_ratio: float = 0.0  # fraction of low-frequency words
    max_sentence_length: int = 0
    type_token_ratio: float = 0.0
    notes: list[str] = field(default_factory=list)

    @property
    def difficulty_label(self) -> str:
        """Human-readable difficulty label."""
        if self.overall_score >= 80:
            return "Very easy"
        elif self.overall_score >= 65:
            return "Easy"
        elif self.overall_score >= 50:
            return "Moderate"
        elif self.overall_score >= 35:
            return "Difficult"
        else:
            return "Very difficult"


# CEFR level thresholds (based on overall score)
CEFR_THRESHOLDS = [
    (80, "A1"),  # Very easy -> A1
    (70, "A2"),  # Easy -> A2
    (55, "B1"),  # Moderate -> B1
    (40, "B2"),  # Challenging -> B2
    (25, "C1"),  # Difficult -> C1
    (0, "C2"),   # Very difficult -> C2
]


def _cefr_from_score(score: float) -> str:
    """Map overall score to CEFR level."""
    for threshold, level in CEFR_THRESHOLDS:
        if score >= threshold:
            return level
    return "C2"


class ReadabilityScorer:
    """Score Luxembourgish text readability.

    Uses dictionary lookup and text statistics to estimate
    reading difficulty. The scoring is heuristic since no
    validated Luxembourgish readability formula exists.
    """

    def __init__(self, wordlist: WordList):
        self.wl = wordlist

    def score(self, text: str) -> ReadabilityScore:
        """Score the readability of a text.

        Args:
            text: Luxembourgish text to score.

        Returns:
            ReadabilityScore with detailed metrics.
        """
        result = ReadabilityScore()

        stats = sentence_stats(text)
        result.word_count = stats["word_count"]
        result.sentence_count = stats["sentence_count"]
        result.avg_sentence_length = stats["avg_sentence_length"]
        result.max_sentence_length = stats["max_sentence_length"]
        result.type_token_ratio = stats["type_token_ratio"]

        if result.word_count == 0:
            result.overall_score = 100.0
            result.cefr_level = "A1"
            result.notes.append("Empty text")
            return result

        # Count unknown words
        tokens = [t for t in tokenize(text) if t.kind == "word"]
        unknown_count = 0
        known_words = []

        for token in tokens:
            if self.wl.is_valid_word(token.text):
                known_words.append(token.text)
            else:
                unknown_count += 1

        result.unknown_ratio = unknown_count / result.word_count

        # Sentence length penalty
        # Average sentence length > 20 words is difficult
        # < 8 words is easy
        if result.avg_sentence_length <= 8:
            length_score = 100.0
        elif result.avg_sentence_length >= 25:
            length_score = 20.0
        else:
            # Linear interpolation between 8 (100) and 25 (20)
            length_score = 100.0 - (80.0 * (result.avg_sentence_length - 8) / 17)

        # Max sentence length penalty
        if result.max_sentence_length > 35:
            length_score *= 0.8
            result.notes.append(f"Very long sentence ({result.max_sentence_length} words)")

        # Unknown word penalty
        # 0% unknown = 100, 20%+ unknown = 0
        unknown_score = max(0.0, 100.0 - (result.unknown_ratio * 500))

        # Type-token ratio bonus
        # Higher TTR means more varied vocabulary = harder
        # TTR > 0.7 is complex, < 0.4 is repetitive
        if result.type_token_ratio > 0.7:
            ttr_score = 30.0
        elif result.type_token_ratio < 0.4:
            ttr_score = 90.0
        else:
            ttr_score = 100.0 - (result.type_token_ratio - 0.4) * 200

        # Composite score (weighted average)
        # Sentence length is the strongest predictor
        result.overall_score = (
            0.40 * length_score
            + 0.35 * unknown_score
            + 0.25 * ttr_score
        )

        # Clamp to 0-100
        result.overall_score = max(0.0, min(100.0, result.overall_score))
        result.cefr_level = _cefr_from_score(result.overall_score)

        # Add notes
        if result.unknown_ratio > 0.15:
            result.notes.append(
                f"High unknown word ratio ({result.unknown_ratio:.1%}) "
                "- text may contain loanwords, proper nouns, or spelling errors"
            )
        if result.avg_sentence_length > 20:
            result.notes.append(
                f"Long average sentence length ({result.avg_sentence_length:.1f} words)"
            )
        if result.type_token_ratio > 0.7 and result.word_count > 50:
            result.notes.append("High lexical diversity")

        return result

    def score_text_level(self, text: str) -> str:
        """Quick helper: return just the CEFR level for a text."""
        return self.score(text).cefr_level
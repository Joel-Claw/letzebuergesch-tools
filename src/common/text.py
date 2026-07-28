"""Common text processing utilities for Luxembourgish.

Handles tokenization, sentence splitting, and normalization.
"""

import re
from dataclasses import dataclass


@dataclass
class Token:
    """A token with its position and type."""
    text: str
    position: int  # Character offset in original text
    kind: str = "word"  # word, punct, number


@dataclass
class Sentence:
    """A sentence with its character span and tokens."""
    text: str
    start: int
    end: int
    tokens: list[Token] = None

    def __post_init__(self):
        if self.tokens is None:
            self.tokens = []


def tokenize(text: str) -> list[Token]:
    """Tokenize Luxembourgish text into words, punctuation, and numbers.

    Handles Luxembourgish special characters (ä, ë, é, ë, ü, ë).
    Elided articles (d') are kept as one token.

    Args:
        text: Input text.

    Returns:
        List of Token objects with positions.
    """
    tokens = []
    # Pattern: words (including Luxembourgish chars and apostrophes), numbers, punctuation
    pattern = re.compile(
        r"(?P<word>[a-zA-Zà-ÿÀ-Ÿ']+)"
        r"|(?P<number>\d+(?:[.,]\d+)*)"
        r"|(?P<punct>[^\w\s])"
    )
    for match in pattern.finditer(text):
        if match.group("word"):
            tokens.append(Token(text=match.group("word"), position=match.start(), kind="word"))
        elif match.group("number"):
            tokens.append(Token(text=match.group("number"), position=match.start(), kind="number"))
        elif match.group("punct"):
            tokens.append(Token(text=match.group("punct"), position=match.start(), kind="punct"))
    return tokens


def split_sentences(text: str) -> list[Sentence]:
    """Split Luxembourgish text into sentences.

    Handles common abbreviations to avoid false splits.
    """
    # Common Luxembourgish abbreviations that don't end sentences
    abbreviations = {
        "z.B.", "Bd.", "Nr.", "S.", "vgl.", "cf.", "etc.",
        "z.T.", "u.a.", "d.h.", " resp.", "ca.", "bzw.",
    }

    # Find potential sentence boundaries
    # A sentence ends with . ! ? followed by whitespace and capital letter
    boundaries = []
    pattern = re.compile(r"([.!?])\s+([A-ZÀ-ÿ])")
    for match in pattern.finditer(text):
        # Check if the text before the period is an abbreviation
        start = max(0, match.start() - 10)
        before = text[start:match.start() + 1]
        is_abbrev = any(before.rstrip().endswith(abbrev) for abbrev in abbreviations)
        if not is_abbrev:
            boundaries.append(match.start() + 1)  # Position of the period

    # Build sentences from boundaries
    sentences = []
    prev_end = 0
    for boundary in boundaries:
        sent_text = text[prev_end:boundary].strip()
        if sent_text:
            sent = Sentence(
                text=sent_text,
                start=prev_end,
                end=boundary,
            )
            sent.tokens = tokenize(sent_text)
            sentences.append(sent)
        prev_end = boundary + 1  # Skip the period

    # Don't forget the last sentence
    if prev_end < len(text):
        sent_text = text[prev_end:].strip()
        if sent_text:
            sent = Sentence(
                text=sent_text,
                start=prev_end,
                end=len(text),
            )
            sent.tokens = tokenize(sent_text)
            sentences.append(sent)

    return sentences


def normalize(text: str) -> str:
    """Normalize Luxembourgish text for comparison.

    - Lowercase
    - Strip trailing/leading whitespace
    - Collapse multiple spaces
    - Normalize apostrophes (curly -> straight)
    """
    # Normalize apostrophes
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def word_frequency(text: str) -> dict[str, int]:
    """Count word frequencies in text.

    Returns:
        Dict mapping lowercased words to their count.
    """
    freq: dict[str, int] = {}
    for token in tokenize(text):
        if token.kind == "word":
            word = token.text.lower()
            freq[word] = freq.get(word, 0) + 1
    return freq


def sentence_stats(text: str) -> dict:
    """Compute basic statistics about the text.

    Returns:
        Dict with: sentence_count, word_count, avg_sentence_length,
        max_sentence_length, unique_words, type_token_ratio
    """
    sentences = split_sentences(text)
    all_words = [t for t in tokenize(text) if t.kind == "word"]

    word_count = len(all_words)
    sentence_count = len(sentences)

    if sentence_count == 0:
        return {
            "sentence_count": 0,
            "word_count": 0,
            "avg_sentence_length": 0,
            "max_sentence_length": 0,
            "unique_words": 0,
            "type_token_ratio": 0.0,
        }

    sent_lengths = [len([t for t in s.tokens if t.kind == "word"]) for s in sentences]
    unique = len(set(w.text.lower() for w in all_words))

    return {
        "sentence_count": sentence_count,
        "word_count": word_count,
        "avg_sentence_length": word_count / sentence_count,
        "max_sentence_length": max(sent_lengths) if sent_lengths else 0,
        "unique_words": unique,
        "type_token_ratio": unique / word_count if word_count > 0 else 0.0,
    }
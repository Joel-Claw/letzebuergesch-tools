"""Grammar checker for Luxembourgish.

Rule-based grammar checking using the ZLS dictionary's part-of-speech and
grammatical tags. Detects common errors: gender agreement, number agreement,
dative case, verb placement.

This is a skeleton implementation that will be expanded with more rules.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from src.wordlist.loader import WordList, WordInfo


@dataclass
class GrammarError:
    """A grammar error found in text."""
    word: str
    position: int  # Character offset in the original text
    message: str
    suggestion: str = ""
    severity: str = "error"  # error, warning, info
    rule: str = ""  # Which rule triggered this


@dataclass
class GrammarResult:
    """Result of a grammar check."""
    errors: list[GrammarError] = field(default_factory=list)
    text: str = ""
    word_count: int = 0

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def error_count(self) -> int:
        return len([e for e in self.errors if e.severity == "error"])

    @property
    def warning_count(self) -> int:
        return len([e for e in self.errors if e.severity == "warning"])


# Luxembourgish articles and their genders
# Nominative articles
# Note: The ZLS dictionary doesn't tag "de" with po:article, so we
# maintain this list explicitly. "d'" is tagged, but "de", "een", "eng",
# "eent" are not.
NOM_ARTICLES = {
    # definite
    "de": "masculine_singular",
    "d'": "feminine_singular",  # elided form (also plural)
    "d": "feminine_singular",   # non-elided (rare but exists)
    "dat": "neutral_singular",
    # plural definite (same as feminine elided, ambiguous)
    # indefinite
    "een": "masculine_singular",
    "eng": "feminine_singular",
    "eent": "neutral_singular",
}

# Words that are articles even if the dictionary doesn't tag them
KNOWN_ARTICLES = {"de", "d'", "d", "dat", "den", "der", "des", "dem",
                   "een", "eng", "eent", "d'", "deem", "dees"}

# Dative articles (used after certain prepositions)
DAT_ARTICLES = {
    "dem": "masculine_singular",  # dative definite masculine
    "der": "feminine_singular",   # dative definite feminine
    "dem": "neutral_singular",    # dative definite neutral (same as masc)
}

# Prepositions that trigger dative case
DATIVE_PREPS = {"aus", "bei", "mat", "mëtt", "no", "zënter", "vun", "zu", "wéinst"}

# Prepositions that can take either dative or accusative
TWO_WAY_PREPS = {"an", "op", "iwwer", "virun", "hanner", "nieft", "tëscht", "ënner"}


class GrammarChecker:
    """Rule-based grammar checker for Luxembourgish.

    Uses the ZLS dictionary to verify part-of-speech tags and check
    grammatical agreement.
    """

    def __init__(self, wordlist: WordList):
        self.wl = wordlist
        self._token_cache: dict[str, list[WordInfo]] = {}

    def _tokenize(self, text: str) -> list[tuple[str, int]]:
        """Split text into tokens with their character positions.

        Returns list of (word, position) tuples.
        """
        tokens = []
        for match in re.finditer(r"[a-zA-ZÀ-ÿ']+", text):
            tokens.append((match.group(), match.start()))
        return tokens

    def _lookup(self, word: str) -> list[WordInfo]:
        """Cached word lookup."""
        if word not in self._token_cache:
            self._token_cache[word] = self.wl.lookup(word)
        return self._token_cache[word]

    def check(self, text: str) -> GrammarResult:
        """Check text for grammar errors.

        Args:
            text: Luxembourgish text to check.

        Returns:
            GrammarResult with all errors found.
        """
        result = GrammarResult(text=text)
        tokens = self._tokenize(text)
        result.word_count = len(tokens)

        # Run all rules
        result.errors.extend(self._check_article_gender_agreement(tokens))
        result.errors.extend(self._check_dative_case(tokens))
        result.errors.extend(self._check_unknown_words(tokens))

        # Sort errors by position
        result.errors.sort(key=lambda e: e.position)
        return result

    def _check_article_gender_agreement(self, tokens: list[tuple[str, int]]) -> list[GrammarError]:
        """Check that articles match the gender of the following noun.

        Example error: "de Haus" (de = masculine, Haus = neutral)
        Should be: "dat Haus"
        """
        errors = []
        article_lower = {k.lower(): v for k, v in NOM_ARTICLES.items()}

        for i, (word, pos) in enumerate(tokens):
            word_lower = word.lower()

            # Check if this word is an article
            if word_lower not in article_lower:
                continue

            # Verify it's actually tagged as article in dictionary
            # Some common articles (de, een, eng) aren't tagged with po:article
            entries = self._lookup(word)
            is_article = (
                any(e.pos == "article" for e in entries)
                or word_lower in KNOWN_ARTICLES
            )
            if not is_article:
                continue

            # Look at the next word
            if i + 1 >= len(tokens):
                continue

            next_word, next_pos = tokens[i + 1]
            next_entries = self._lookup(next_word)

            # Find the noun entry
            noun_entry = None
            for entry in next_entries:
                if entry.pos == "noun":
                    noun_entry = entry
                    break

            if noun_entry is None:
                continue

            article_gender = article_lower[word_lower]
            noun_gender = noun_entry.gender

            if not noun_gender:
                continue

            # Check agreement
            # Article gender like "masculine_singular" should match noun gender
            if article_gender != noun_gender:
                # Find the correct article
                correct_article = None
                for art, gender in article_lower.items():
                    if gender == noun_gender:
                        correct_article = art
                        break

                errors.append(GrammarError(
                    word=word,
                    position=pos,
                    message=f"Article gender mismatch: '{word}' ({article_gender}) with '{next_word}' ({noun_gender})",
                    suggestion=correct_article or "",
                    severity="error",
                    rule="article_gender_agreement",
                ))

        return errors

    def _check_dative_case(self, tokens: list[tuple[str, int]]) -> list[GrammarError]:
        """Check for dative case errors after dative prepositions.

        After dative prepositions (aus, bei, mat, no, vun, zu, wéinst),
        articles should be in dative form (dem, der, etc.) not nominative (de, d').
        """
        errors = []

        for i, (word, pos) in enumerate(tokens):
            word_lower = word.lower()

            if word_lower not in DATIVE_PREPS:
                continue

            # Check the next word - should be a dative article if it's an article
            if i + 1 >= len(tokens):
                continue

            next_word, next_pos = tokens[i + 1]
            next_lower = next_word.lower()

            # If next word is a nominative article, that's a potential error
            if next_lower in NOM_ARTICLES and next_lower not in DAT_ARTICLES:
                entries = self._lookup(next_word)
                is_article = (
                    any(e.pos == "article" for e in entries)
                    or next_lower in KNOWN_ARTICLES
                )
                if is_article:
                    # Determine what the dative form should be
                    noun_gender = None
                    if i + 2 < len(tokens):
                        noun_entries = self._lookup(tokens[i + 2][0])
                        for entry in noun_entries:
                            if entry.pos == "noun":
                                noun_gender = entry.gender
                                break

                    if noun_gender:
                        if "masculine" in noun_gender or "neutral" in noun_gender:
                            suggestion = "dem"
                        elif "feminine" in noun_gender:
                            suggestion = "der"
                        else:
                            suggestion = "dem"
                    else:
                        suggestion = "dem"

                    errors.append(GrammarError(
                        word=next_word,
                        position=next_pos,
                        message=f"Dative case error: '{word_lower}' requires dative article, got nominative '{next_word}'",
                        suggestion=suggestion,
                        severity="error",
                        rule="dative_after_preposition",
                    ))

        return errors

    def _check_unknown_words(self, tokens: list[tuple[str, int]]) -> list[GrammarError]:
        """Flag words not found in the dictionary.

        These might be spelling errors, loanwords, or proper nouns.
        Marked as 'info' severity since proper nouns and loanwords are common.
        """
        errors = []

        for word, pos in tokens:
            if not self.wl.is_valid_word(word):
                # Skip very short words (might be fragments from tokenization)
                if len(word) <= 1:
                    continue
                # Skip words that look like proper nouns (start with uppercase, not at start of sentence)
                if word[0].isupper() and pos > 0:
                    continue
                errors.append(GrammarError(
                    word=word,
                    position=pos,
                    message=f"Unknown word: '{word}' not found in dictionary",
                    suggestion="",
                    severity="info",
                    rule="unknown_word",
                ))

        return errors
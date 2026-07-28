"""Luxembourgish text normalization.

Handles spelling variant normalization using the ZLS dictionary's
variant information and known orthographic alternatives.

Luxembourgish has several spelling conventions that produce variants:
- "E" vs "ë" in certain positions (e.g., "Kichen" vs "Kiche")
- "sch" vs "sh" (rare, mostly older texts)
- "é" vs "ee" (e.g., "wéen" vs "ween" — not always equivalent)
- "ai" vs "ei" (e.g., "Mais" vs "Meis" — context dependent)
- Apostrophe forms: d' vs d' vs d'
- Hyphenated compounds: Z-Bahn vs Zuchtbahn

This module provides:
1. Orthographic normalization (variant -> standard form)
2. Punctuation/whitespace normalization
3. Case normalization for comparison purposes

References:
- spellux project (github.com/spellchecker-lu/spellux)
- R. Lutgen et al., "Orthography of the Luxembourgish Language" (ZLS)
- ZLS dictionary variant tags (po:variant, alt forms)
"""

import re
from dataclasses import dataclass
from pathlib import Path

from src.wordlist.loader import WordList


@dataclass
class NormalizationResult:
    """Result of normalizing a text."""
    original: str
    normalized: str
    changes: list  # List of (position, original_word, normalized_word)
    change_count: int


class Normalizer:
    """Normalizes Luxembourgish text to standard orthography.

    Uses the ZLS dictionary to identify and correct spelling variants.
    Falls back to rule-based heuristics for variants not in the dictionary.
    """

    # Known variant mappings (non-exhaustive, based on ZLS conventions)
    # These are applied when a word is not found in the dictionary but
    # a known variant mapping produces a dictionary word.
    VARIANT_RULES = {
        # Common apostrophe variations
        "d'": "d'",
        "D'": "D'",
        # Double consonant simplification (rare, but some texts use single)
        # We do NOT do this by default — it's too aggressive

        # "ue" -> "ue" (no change, but some old texts write "uë")
        # "ae" -> "ä" (older orthography)
    }

    # Common misspellings -> standard forms
    COMMON_FIXES = {
        "lëtzebuergesch": "lëtzebuergesch",
        "Lëtzebuerg": "Lëtzebuerg",
        "lëtzebuerg": "Lëtzebuerg",
        # Capitalization fixes for proper nouns
        "däitschland": "Däitschland",
        "frankräich": "Frankräich",
        "belsch": "Belsch",
    }

    def __init__(self, wordlist: WordList | None = None):
        """Initialize the normalizer.

        Args:
            wordlist: Optional ZLS dictionary for variant lookup.
                      If None, only rule-based normalization is applied.
        """
        self.wordlist = wordlist
        self._variant_map: dict[str, str] = {}
        if wordlist:
            self._build_variant_map()

    def _build_variant_map(self):
        """Build a mapping from variant forms to standard forms."""
        # The ZLS dictionary contains base forms in _base_words
        # and conjugated forms in _conjugated. We use _all_words for lookup.
        # Build a map from common variant spellings to canonical forms.
        self._variant_map.update(self.COMMON_FIXES)

    def normalize_text(self, text: str) -> NormalizationResult:
        """Normalize a full text to standard Luxembourgish orthography.

        Args:
            text: Input text with possible spelling variants.

        Returns:
            NormalizationResult with the normalized text and list of changes.
        """
        changes = []
        result = text

        # Step 1: Unicode normalization (NFC)
        import unicodedata
        result = unicodedata.normalize("NFC", result)

        # Step 2: Apostrophe normalization (curly -> straight)
        result = result.replace("\u2019", "'").replace("\u2018", "'")

        # Step 3: Quote normalization
        result = result.replace("\u201c", '"').replace("\u201d", '"')
        result = result.replace("\u00bb", "»").replace("\u00ab", "«")

        # Step 4: Whitespace normalization
        result = re.sub(r"[ \t]+", " ", result)  # Collapse spaces/tabs
        result = re.sub(r"\n{3,}", "\n\n", result)  # Max 2 newlines
        result = re.sub(r" \n", "\n", result)  # No space before newline
        result = result.strip()

        # Step 5: Word-level normalization
        # Find words and check if they need fixing
        word_pattern = re.compile(r"[a-zA-Zà-ÿÀ-Ÿ']+")

        def replace_word(match):
            word = match.group()
            lower = word.lower()

            # Check common fixes first
            if lower in self._variant_map:
                fixed = self._variant_map[lower]
                # Preserve original capitalization pattern
                if word[0].isupper():
                    fixed = fixed[0].upper() + fixed[1:]
                if word.isupper():
                    fixed = fixed.upper()
                if fixed != word:
                    changes.append((match.start(), word, fixed))
                return fixed

            # Check if word is in dictionary
            if self.wordlist:
                entries = self.wordlist.lookup(word)
                if not entries:
                    # Try lowercase
                    entries = self.wordlist.lookup(lower)
                    if entries:
                        # Word exists but wrong case — don't fix case automatically
                        pass

                    # Try common variant transformations
                    candidate = self._try_variants(lower)
                    if candidate and candidate != lower:
                        # Preserve capitalization
                        if word[0].isupper():
                            candidate = candidate[0].upper() + candidate[1:]
                        if word.isupper():
                            candidate = candidate.upper()
                        if candidate != word:
                            # Verify the candidate is in the dictionary
                            if self.wordlist.lookup(candidate):
                                changes.append((match.start(), word, candidate))
                                return candidate

            return word

        result = word_pattern.sub(replace_word, result)

        return NormalizationResult(
            original=text,
            normalized=result,
            changes=changes,
            change_count=len(changes),
        )

    def _try_variants(self, word: str) -> str | None:
        """Try common variant transformations to find a dictionary match.

        Args:
            word: A lowercase word not found in the dictionary.

        Returns:
            A candidate standard form if one is found, else None.
        """
        candidates = []

        # 1. uë -> ue (older orthography)
        if "uë" in word:
            candidates.append(word.replace("uë", "ue"))

        # 2. aë -> ae -> ä (older orthography)
        if "aë" in word:
            candidates.append(word.replace("aë", "ä"))

        # 3. Double ee -> single e (some older texts double vowels)
        # Skip — too aggressive, creates false positives

        # 4. ai -> ei (common variant in some dialects)
        if "ai" in word:
            candidates.append(word.replace("ai", "ei"))

        # 5. ss -> ß (German influence, very rare in modern Luxembourgish)
        # Skip — Luxembourgish doesn't use ß

        # 6. ae -> ä (old spelling without diacritics)
        if "ae" in word:
            candidates.append(word.replace("ae", "ä"))
        if "oe" in word:
            candidates.append(word.replace("oe", "ö"))
        if "ue" in word and "uë" not in word:
            candidates.append(word.replace("ue", "ü"))

        # 7. Remove trailing 'e' that might be silent (some dialects add it)
        # Skip — too aggressive

        # Check candidates against dictionary
        for candidate in candidates:
            if self.wordlist and self.wordlist.lookup(candidate):
                return candidate

        return None

    def normalize_word(self, word: str) -> str:
        """Normalize a single word to its standard form.

        Args:
            word: Input word.

        Returns:
            Normalized word.
        """
        result = self.normalize_text(word)
        return result.normalized
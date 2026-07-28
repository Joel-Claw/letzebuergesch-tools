"""ZLS spellchecker word list loader and query interface.

Loads the official ZLS HunSpell dictionary files (lb_LU.dic and unmunched.dic)
and provides fast word lookup with part-of-speech and grammatical information.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class WordInfo:
    """Information about a word from the ZLS dictionary."""
    word: str
    pos: str = ""  # noun, verb, adjective, adverb, article, conjunction, etc.
    gender: str = ""  # feminine_singular, masculine_plural, neutral_singular, etc.
    tags: list[str] = field(default_factory=list)  # All tags from the dictionary entry
    is_valid: bool = True


class WordList:
    """Loader and query interface for the ZLS Luxembourgish word list.

    Loads from the HunSpell dictionary files. The .dic file contains base forms
    with part-of-speech tags. The unmunched.dic contains all conjugated forms.
    """

    # Tag patterns
    POS_PATTERN = re.compile(r'po:(\w+)')
    GENDER_PATTERN = re.compile(r'ts:(\w+(?:_\w+)?)')

    @classmethod
    def from_dictionary(cls, dict_path: str | Path) -> 'WordList':
        """Create a WordList from a dictionary directory.

        Args:
            dict_path: Path to the dictionary-lb-lu directory containing
                      lb_LU.dic and unmunched.dic.

        Returns:
            WordList instance.
        """
        return cls(dict_path=dict_path)

    def __init__(self, dict_path: str | Path | None = None):
        """Load the dictionary.

        Args:
            dict_path: Path to the dictionary-lb-lu directory.
                      Defaults to ../data/dictionary-lb-lu relative to this file.
        """
        if dict_path is None:
            dict_path = Path(__file__).parent.parent.parent / "data" / "dictionary-lb-lu"
        self.dict_path = Path(dict_path)

        # word -> list of WordInfo (a word can have multiple entries)
        self._base_words: dict[str, list[WordInfo]] = {}
        # All known words (base + conjugated) for fast valid-word lookup
        self._all_words: set[str] = set()
        # word -> list of WordInfo for conjugated forms (from unmunched.dic)
        self._conjugated: dict[str, list[WordInfo]] = {}

        self._load_base()
        self._load_conjugated()

    def _parse_entry(self, line: str) -> WordInfo | None:
        """Parse a single dictionary entry line.

        Format examples:
            Haus/n0 po:noun ts:neutral_singular
            goen/f6 po:verb
            schéin/a0 po:adjective
            an po:conjunction
        """
        line = line.strip()
        if not line:
            return None

        # Split word from tags (tags start after the word + optional affix codes)
        # The format is: word/affix_codes tag1 tag2 ...
        # Some entries have no tags at all (just the word)
        parts = line.split()

        if len(parts) == 0:
            return None

        # First part is word/affix_codes
        first = parts[0]
        if '/' in first:
            word = first.split('/')[0]
        else:
            word = first

        # Extract tags
        pos = ""
        gender = ""
        tags = []

        for part in parts[1:]:
            tags.append(part)
            pos_match = self.POS_PATTERN.search(part)
            if pos_match:
                pos = pos_match.group(1)
            gender_match = self.GENDER_PATTERN.search(part)
            if gender_match:
                gender = gender_match.group(1)

        return WordInfo(word=word, pos=pos, gender=gender, tags=tags)

    def _load_base(self):
        """Load base/stem forms from lb_LU.dic."""
        dic_file = self.dict_path / "lb_LU.dic"
        if not dic_file.exists():
            raise FileNotFoundError(f"Dictionary file not found: {dic_file}")

        with open(dic_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue  # First line is the word count
                entry = self._parse_entry(line)
                if entry:
                    self._base_words.setdefault(entry.word.lower(), []).append(entry)
                    self._all_words.add(entry.word.lower())

    def _load_conjugated(self):
        """Load all conjugated/expanded forms from unmunched.dic."""
        dic_file = self.dict_path / "unmunched.dic"
        if not dic_file.exists():
            # unmunched.dic is optional, base forms are enough for basic lookup
            return

        with open(dic_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line[0].isdigit():
                    continue
                # unmunched.dic entries may not have tags, just the word
                entry = self._parse_entry(line)
                if entry:
                    self._all_words.add(entry.word.lower())
                    if entry.pos or entry.gender:
                        self._conjugated.setdefault(entry.word.lower(), []).append(entry)

    def lookup(self, word: str) -> list[WordInfo]:
        """Look up a word and return all matching entries.

        Args:
            word: The word to look up (case-insensitive).

        Returns:
            List of WordInfo entries. Empty list if not found.
        """
        word_lower = word.lower()
        results = []

        # Check base forms first
        if word_lower in self._base_words:
            results.extend(self._base_words[word_lower])

        # Check conjugated forms
        if word_lower in self._conjugated:
            results.extend(self._conjugated[word_lower])

        # If no tagged entries found but word is in the set, return a basic valid entry
        if not results and word_lower in self._all_words:
            results.append(WordInfo(word=word, is_valid=True))

        return results

    def is_valid_word(self, word: str) -> bool:
        """Check if a word exists in the dictionary.

        Args:
            word: The word to check (case-insensitive).

        Returns:
            True if the word is a valid Luxembourgish word.
        """
        return word.lower() in self._all_words

    def get_pos(self, word: str) -> str | None:
        """Get the part of speech of a word.

        Returns:
            Part of speech string (e.g. 'noun', 'verb') or None if unknown.
        """
        entries = self.lookup(word)
        for entry in entries:
            if entry.pos:
                return entry.pos
        return None

    def get_gender(self, word: str) -> str | None:
        """Get the grammatical gender of a noun.

        Returns:
            Gender string (e.g. 'masculine_singular') or None if not a noun or unknown.
        """
        entries = self.lookup(word)
        for entry in entries:
            if entry.gender and entry.pos == 'noun':
                return entry.gender
        return None

    def is_noun(self, word: str) -> bool:
        """Check if a word is a noun."""
        return self.get_pos(word) == 'noun'

    def is_verb(self, word: str) -> bool:
        """Check if a word is a verb."""
        return self.get_pos(word) == 'verb'

    def is_adjective(self, word: str) -> bool:
        """Check if a word is an adjective."""
        return self.get_pos(word) == 'adjective'

    def is_article(self, word: str) -> bool:
        """Check if a word is an article."""
        return self.get_pos(word) == 'article'

    def __len__(self) -> int:
        """Total number of unique words (base + conjugated)."""
        return len(self._all_words)

    def get_by_pos(self, pos: str) -> list[str]:
        """Get all words of a specific part of speech.

        Args:
            pos: Part of speech (e.g. 'noun', 'verb', 'adjective').

        Returns:
            List of words matching the POS.
        """
        result = []
        for word, entries in self._base_words.items():
            for entry in entries:
                if entry.pos == pos:
                    result.append(entry.word)
                    break
        return result

    @property
    def word_count(self) -> int:
        """Total number of unique words (base + conjugated)."""
        return len(self._all_words)

    @property
    def base_word_count(self) -> int:
        """Number of base/stem forms."""
        return len(self._base_words)

    def nouns_by_gender(self, gender: str) -> list[str]:
        """Get all nouns of a specific gender.

        Args:
            gender: Gender string, e.g. 'masculine_singular'.

        Returns:
            List of noun words matching the gender.
        """
        result = []
        for word, entries in self._base_words.items():
            for entry in entries:
                if entry.pos == 'noun' and entry.gender == gender:
                    result.append(entry.word)
                    break
        return result
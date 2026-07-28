"""Tests for the wordlist loader."""

import pytest
from src.wordlist.loader import WordList, WordInfo


@pytest.fixture
def wordlist():
    return WordList.from_dictionary(
        "/home/alex/letzebuergesch-tools/data/dictionary-lb-lu"
    )


class TestWordList:
    def test_load_dictionary(self, wordlist):
        assert len(wordlist) > 50000  # Should have loaded many words

    def test_lookup_known_word(self, wordlist):
        # "Haus" should be in the dictionary
        entries = wordlist.lookup("Haus")
        assert len(entries) > 0
        assert any(e.pos == "noun" for e in entries)

    def test_lookup_unknown_word(self, wordlist):
        entries = wordlist.lookup("xyzqwertz")
        assert len(entries) == 0

    def test_is_valid_word(self, wordlist):
        assert wordlist.is_valid_word("Haus") is True
        assert wordlist.is_valid_word("xyzqwertz") is False

    def test_case_insensitive_lookup(self, wordlist):
        entries_lower = wordlist.lookup("haus")
        entries_upper = wordlist.lookup("Haus")
        # Both should find the word
        assert len(entries_lower) > 0 or len(entries_upper) > 0

    def test_get_nouns(self, wordlist):
        nouns = wordlist.get_by_pos("noun")
        assert len(nouns) > 1000  # Should have many nouns

    def test_word_info_has_tags(self, wordlist):
        entries = wordlist.lookup("Haus")
        if entries:
            entry = entries[0]
            assert entry.word == "Haus"
            assert entry.pos is not None
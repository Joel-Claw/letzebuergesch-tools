"""Tests for the grammar checker."""

import pytest
from src.wordlist.loader import WordList
from src.grammar.checker import GrammarChecker, GrammarResult


@pytest.fixture
def wordlist():
    """Load the ZLS dictionary for testing."""
    return WordList.from_dictionary(
        "/home/alex/letzebuergesch-tools/data/dictionary-lb-lu"
    )


@pytest.fixture
def checker(wordlist):
    return GrammarChecker(wordlist)


class TestTokenization:
    def test_simple_sentence(self, checker):
        tokens = checker._tokenize("D'Kommereze steet zu Lëtzebuerg.")
        assert len(tokens) >= 3
        assert tokens[0][0] == "D'Kommereze"

    def test_special_chars(self, checker):
        tokens = checker._tokenize("D'Kirmesdagsfeier")
        assert len(tokens) == 1
        assert tokens[0][0] == "D'Kirmesdagsfeier"

    def test_empty_string(self, checker):
        tokens = checker._tokenize("")
        assert len(tokens) == 0


class TestUnknownWords:
    def test_known_word_no_error(self, checker):
        result = checker.check("Haus")
        # "Haus" should be in the dictionary
        unknown_errors = [e for e in result.errors if e.rule == "unknown_word"]
        assert len(unknown_errors) == 0

    def test_gibberish_flagged(self, checker):
        result = checker.check("xyzqwertz")
        unknown_errors = [e for e in result.errors if e.rule == "unknown_word"]
        assert len(unknown_errors) == 1

    def test_proper_noun_not_flagged(self, checker):
        # Words starting with uppercase (not at position 0) should be skipped
        result = checker.check("Ech sinn Max.")
        unknown_errors = [e for e in result.errors if e.rule == "unknown_word"]
        assert len(unknown_errors) == 0


class TestDativeCase:
    def test_dative_preposition_correct(self, checker):
        # "mat dem Auto" - dem is dative, correct
        result = checker.check("mat dem Auto")
        dative_errors = [e for e in result.errors if e.rule == "dative_after_preposition"]
        assert len(dative_errors) == 0

    def test_dative_preposition_wrong(self, checker):
        # "mat de Auto" - de is nominative, should be dem
        result = checker.check("mat de Auto")
        dative_errors = [e for e in result.errors if e.rule == "dative_after_preposition"]
        assert len(dative_errors) == 1
        assert dative_errors[0].suggestion == "dem"


class TestResult:
    def test_empty_text(self, checker):
        result = checker.check("")
        assert result.word_count == 0
        assert len(result.errors) == 0
        assert not result.has_errors

    def test_error_count(self, checker):
        result = checker.check("mat de Auto mat de Haus")
        assert result.error_count >= 2
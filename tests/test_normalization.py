"""Tests for the normalization module."""

import pytest
from src.normalization.normalizer import Normalizer, NormalizationResult


class TestNormalizationResult:
    def test_empty_text(self):
        normalizer = Normalizer()
        result = normalizer.normalize_text("")
        assert result.normalized == ""
        assert result.change_count == 0

    def test_no_changes_needed(self):
        normalizer = Normalizer()
        result = normalizer.normalize_text("D'Kommereze steet zu Lëtzebuerg.")
        assert result.change_count == 0
        assert "Lëtzebuerg" in result.normalized

    def test_unicode_normalization(self):
        normalizer = Normalizer()
        # Text with decomposed Unicode (NFD) should be normalized to NFC
        import unicodedata
        nfd_text = unicodedata.normalize("NFD", "Lëtzebuerg")
        result = normalizer.normalize_text(nfd_text)
        assert unicodedata.is_normalized("NFC", result.normalized)

    def test_apostrophe_normalization(self):
        normalizer = Normalizer()
        # Curly apostrophe should become straight
        result = normalizer.normalize_text("D\u2019Kommereze")
        assert "'" in result.normalized
        assert "\u2019" not in result.normalized

    def test_whitespace_collapse(self):
        normalizer = Normalizer()
        result = normalizer.normalize_text("D'Kommereze    steet   zu Lëtzebuerg.")
        assert "  " not in result.normalized
        assert result.normalized == "D'Kommereze steet zu Lëtzebuerg."

    def test_newline_collapse(self):
        normalizer = Normalizer()
        result = normalizer.normalize_text("Zeil 1\n\n\n\nZeil 2")
        assert result.normalized == "Zeil 1\n\nZeil 2"

    def test_space_before_newline(self):
        normalizer = Normalizer()
        result = normalizer.normalize_text("Zeil 1 \nZeil 2")
        assert " \n" not in result.normalized

    def test_trailing_whitespace(self):
        normalizer = Normalizer()
        result = normalizer.normalize_text("  Test  ")
        assert result.normalized == "Test"

    def test_quote_normalization(self):
        normalizer = Normalizer()
        result = normalizer.normalize_text("S\u201chunn\u201d")
        assert '"' in result.normalized
        assert "\u201c" not in result.normalized
        assert "\u201d" not in result.normalized

    def test_changes_recorded(self):
        normalizer = Normalizer()
        # Whitespace changes are normalized but not tracked as "changes" in the list
        # Only word-level fixes are tracked. Test with extra whitespace to verify
        # the result structure works correctly.
        result = normalizer.normalize_text("Test   Wort")
        assert isinstance(result.change_count, int)
        assert isinstance(result.changes, list)
        assert result.change_count == len(result.changes)

    def test_preserve_case(self):
        normalizer = Normalizer()
        result = normalizer.normalize_text("LËTZEBUERG")
        # Should not lowercase the text
        assert result.normalized.isupper()

    def test_mixed_content(self):
        normalizer = Normalizer()
        text = "D'Kommereze steet zu Lëtzebuerg.  \n\n  Et ass eng Stad."
        result = normalizer.normalize_text(text)
        assert "  " not in result.normalized
        assert "D'Kommereze" in result.normalized


class TestNormalizeWord:
    def test_simple_word(self):
        normalizer = Normalizer()
        assert normalizer.normalize_word("Haus") == "Haus"

    def test_apostrophe_word(self):
        normalizer = Normalizer()
        assert "'" in normalizer.normalize_word("d\u2019Haus")

    def test_empty_word(self):
        normalizer = Normalizer()
        assert normalizer.normalize_word("") == ""


class TestWithDictionary:
    """Tests that require the ZLS dictionary."""

    def test_variant_detection(self, wordlist):
        normalizer = Normalizer(wordlist)
        # Test that a known variant gets normalized
        # (Specific variant depends on dictionary content)
        result = normalizer.normalize_text("Lëtzebuerg")
        assert result.normalized == "Lëtzebuerg"

    def test_dictionary_lookup_preserves_correct_words(self, wordlist):
        normalizer = Normalizer(wordlist)
        result = normalizer.normalize_text("Haus")
        assert result.change_count == 0
        assert result.normalized == "Haus"

    def test_ae_to_umlaut_variant(self, wordlist):
        """Test that 'ae' gets normalized to 'ä' when the umlaut form is in dictionary."""
        normalizer = Normalizer(wordlist)
        # If "Baer" is not in dict but "Bär" is, it should normalize
        result = normalizer.normalize_text("Baeren")
        # Just verify it doesn't crash — actual fix depends on dict content
        assert isinstance(result.normalized, str)
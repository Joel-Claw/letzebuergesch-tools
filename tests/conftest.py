"""Shared test fixtures for Lëtzebuergesch Tools."""

import os
from pathlib import Path

import pytest

from src.wordlist.loader import WordList

# Path to dictionary data (gitignored, may not exist on CI)
DICT_PATH = Path(__file__).parent.parent / "data" / "dictionary-lb-lu"

# Check if dictionary data is available
HAS_DICTIONARY = DICT_PATH.exists() and (DICT_PATH / "unmunched.dic").exists()


@pytest.fixture
def wordlist():
    """Load the ZLS dictionary for testing. Skips if dictionary data not present."""
    if not HAS_DICTIONARY:
        pytest.skip("ZLS dictionary data not available (see data/README.md)")
    return WordList.from_dictionary(str(DICT_PATH))


@pytest.fixture
def dict_path():
    """Return the dictionary path, skipping if not available."""
    if not HAS_DICTIONARY:
        pytest.skip("ZLS dictionary data not available (see data/README.md)")
    return str(DICT_PATH)
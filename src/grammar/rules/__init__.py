"""Grammar rules for Luxembourgish.

Individual rule modules that can be used by the GrammarChecker.
Each rule module provides a check function that takes tokens and
returns a list of GrammarError objects.
"""

from src.grammar.checker import GrammarError
from src.wordlist.loader import WordList
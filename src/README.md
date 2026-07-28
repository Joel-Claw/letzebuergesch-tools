# Lëtzebuergesch Tools - Source Code

## Structure

```
src/
├── wordlist/          # ZLS dictionary loader and word lookup
│   ├── __init__.py
│   └── loader.py      # Load and query lb_LU.dic / unmunched.dic
├── grammar/           # Grammar checker (rule-based)
│   ├── __init__.py
│   ├── checker.py     # Main grammar checking engine
│   └── rules/         # Grammar rule definitions
│       ├── __init__.py
│       ├── agreement.py    # Article-noun gender/number agreement
│       ├── dative.py       # Dative case detection (common error)
│       └── word_order.py   # Verb placement rules
├── readability/       # Readability scorer
│   ├── __init__.py
│   └── scorer.py      # CEFR-aligned text difficulty scoring
└── common/            # Shared utilities
    ├── __init__.py
    └── text.py        # Text processing utilities
```

## Dependencies

- Python 3.11+
- ZLS spellchecker data in `data/dictionary-lb-lu/` (see `data/README.md`)

## Usage

```python
from src.wordlist import WordList
from src.grammar import GrammarChecker
from src.readability import ReadabilityScorer

# Load dictionary
wl = WordList()

# Check a word
info = wl.lookup("Haus")
# -> WordInfo(word="Haus", pos="noun", gender="neutral_singular", ...)

# Grammar check
checker = GrammarChecker(wordlist=wl)
errors = checker.check("D'Haus ass schéin.")
# -> [GrammarError(message="Wrong article gender: de (masculine) used with Haus (neutral)")]

# Readability
scorer = ReadabilityScorer(wordlist=wl)
score = scorer.score("D'Haus ass schéin.")
# -> ReadabilityScore(level="A1", score=0.95, ...)
```
"""Dative case detection rule for Luxembourgish.

After dative prepositions (aus, bei, mat, no, vun, zu, wéinst),
articles must be in dative form (dem, der) rather than nominative (de, d').

Example:
    mat de Auto  -> ERROR (de = nominative, should be dem)
    mat dem Auto -> OK
"""

from src.grammar.checker import GrammarError, NOM_ARTICLES, DAT_ARTICLES, KNOWN_ARTICLES

# Prepositions that always trigger dative case
DATIVE_PREPS = {"aus", "bei", "mat", "mëtt", "no", "zënter", "vun", "zu", "wéinst"}


def check(tokens: list[tuple[str, int]], wordlist: WordList) -> list[GrammarError]:
    """Check for dative case errors after dative prepositions.

    Args:
        tokens: List of (word, position) tuples.
        wordlist: Loaded ZLS dictionary.

    Returns:
        List of GrammarError objects for dative violations.
    """
    errors = []

    for i, (word, pos) in enumerate(tokens):
        word_lower = word.lower()

        if word_lower not in DATIVE_PREPS:
            continue

        if i + 1 >= len(tokens):
            continue

        next_word, next_pos = tokens[i + 1]
        next_lower = next_word.lower()

        # If next word is a nominative article, that's an error
        if next_lower in NOM_ARTICLES and next_lower not in DAT_ARTICLES:
            entries = wordlist.lookup(next_word)
            is_article = (
                any(e.pos == "article" for e in entries)
                or next_lower in KNOWN_ARTICLES
            )
            if not is_article:
                continue

            # Determine correct dative article based on following noun
            noun_gender = None
            if i + 2 < len(tokens):
                noun_entries = wordlist.lookup(tokens[i + 2][0])
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
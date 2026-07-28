"""Article-noun gender agreement rule for Luxembourgish.

Checks that articles match the grammatical gender of the following noun.

Examples:
    de Haus  -> ERROR (de = masculine, Haus = neutral)
    dat Haus -> OK
    eng Auto -> ERROR (eng = feminine, Auto = masculine)
    een Auto -> OK
"""

from src.grammar.checker import GrammarError, NOM_ARTICLES, KNOWN_ARTICLES


def check(tokens: list[tuple[str, int]], wordlist: WordList) -> list[GrammarError]:
    """Check article-noun gender agreement.

    Args:
        tokens: List of (word, position) tuples.
        wordlist: Loaded ZLS dictionary.

    Returns:
        List of GrammarError objects for mismatches.
    """
    errors = []
    article_lower = {k.lower(): v for k, v in NOM_ARTICLES.items()}

    for i, (word, pos) in enumerate(tokens):
        word_lower = word.lower()

        if word_lower not in article_lower:
            continue

        # Verify it's an article
        entries = wordlist.lookup(word)
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
        next_entries = wordlist.lookup(next_word)

        noun_entry = None
        for entry in next_entries:
            if entry.pos == "noun":
                noun_entry = entry
                break

        if noun_entry is None or not noun_entry.gender:
            continue

        article_gender = article_lower[word_lower]
        noun_gender = noun_entry.gender

        if article_gender != noun_gender:
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
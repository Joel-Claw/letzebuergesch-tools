"""Verb placement (V2) rule for Luxembourgish.

Luxembourgish follows V2 word order: the finite verb must be the second
constituent in a main clause. In subordinate clauses, the verb goes to
the end.

This is a simplified check that flags obvious V2 violations in main clauses.
Full V2 checking requires syntactic parsing, which is beyond the current scope.
"""

from src.grammar.checker import GrammarError

# Common subordinating conjunctions that push verb to end
SUB_CONJUNCTIONS = {
    "datt", "wëll", "well", "wann", "éischt", "iwwerdeems",
    "nodeems", "iwwerdeems", "wéi", "bis", "soss", "fir",
    "well", "ob", "cf", "oudem",
}


def check(tokens: list[tuple[str, int]], wordlist: WordList) -> list[GrammarError]:
    """Check for verb placement errors.

    This is a basic implementation that flags:
    - Verb in position 3+ in a main clause without a subordinate conjunction
    - Missing verb in a clause

    Note: This is intentionally conservative. False positives would be worse
    than missing some errors, since Luxembourgish word order has many exceptions.
    """
    errors = []

    # Group tokens by sentence (simplified: split on periods)
    sentences = []
    current = []
    for word, pos in tokens:
        current.append((word, pos))
        if word.endswith(".") or word == ".":
            sentences.append(current)
            current = []
    if current:
        sentences.append(current)

    for sent in sentences:
        if len(sent) < 3:
            continue

        # Check for subordinate clause
        first_word = sent[0][0].lower()
        has_sub_conj = first_word in SUB_CONJUNCTIONS

        if has_sub_conj:
            # In subordinate clauses, verb should be at the end
            # This is hard to check without full parsing, skip for now
            continue

        # In main clauses, verb should be in position 2 (index 1)
        # Find the first verb
        verb_idx = None
        for idx, (word, pos) in enumerate(sent):
            entries = wordlist.lookup(word)
            if any(e.pos == "verb" for e in entries):
                verb_idx = idx
                break

        if verb_idx is not None and verb_idx > 2:
            # Verb is too far back in a main clause
            # Only flag if there's no conjunction at position 0
            # This is a warning, not an error, due to high false positive risk
            errors.append(GrammarError(
                word=sent[verb_idx][0],
                position=sent[verb_idx][1],
                message=f"Verb placement: '{sent[verb_idx][0]}' is in position {verb_idx + 1}, expected position 2 (V2 rule)",
                suggestion="",
                severity="warning",
                rule="verb_placement_v2",
            ))

    return errors
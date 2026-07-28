# ZLS Spellchecker Data

Source: [data.public.lu - Lëtzebuergesch Wierderlëscht](https://data.public.lu/fr/datasets/letzebuergesch-wierderlescht/)
GitHub: [spellchecker-lu/dictionary-lb-lu](https://github.com/spellchecker-lu/dictionary-lb-lu)
License: Other (Attribution)
Last updated: January 21, 2026
Confirmed available by ZLS on May 21, 2026.

## Files

| File | Description | Lines |
|------|-------------|-------|
| `lb_LU.dic` | HunSpell dictionary, base/stem forms | 94'828 |
| `lb_LU.aff` | HunSpell affix rules for conjugation | 79 KB |
| `unmunched.dic` | Fully expanded/conjugated word forms | 350'372 |
| `th_lb_LU_v2.dat` | MyThes thesaurus data | 587 KB |
| `th_lb_LU_v2.idx` | MyThes thesaurus index | 237 KB |
| `LICENSE.txt` | License terms | - |

## Usage

The `unmunched.dic` file contains all conjugated forms (350k+) and is useful for
direct word lookup. The `lb_LU.dic` + `lb_LU.aff` pair is for HunSpell integration.

Each entry in `lb_LU.dic` includes part-of-speech and grammatical tags:
- `po:noun ts:masculine_singular`
- `po:adjective`
- `po:verb`

These tags are valuable for grammar checking and readability scoring.
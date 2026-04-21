# Security Policy

## Reporting Vulnerabilities

This is an early-stage language tools project. If you find a security issue:

1. Open a GitHub issue with the `security` label
2. Do not publicly disclose exploitable vulnerabilities before they are fixed

## Data Handling

- This project does not collect personal data
- Tools that process text (spell checking, grammar checking) should do so locally when possible
- If API calls to external services (LOD, spellchecker.lu) are needed, no user text should be logged

## Third-Party Dependencies

- LOD API (api.lod.lu) - government dictionary service
- spellchecker.lu - HunSpell dictionary (local)
- ZLS models on HuggingFace - speech/text models (optional)

Each dependency has its own terms of use. Check before integrating.

## Status

This project is in alpha. There may be bugs, incomplete features, and rough edges. Use accordingly.
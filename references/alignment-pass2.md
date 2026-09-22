# Alignment pass 2

[Family guide](skill-family.md) · [Branding and handoffs](../BRANDING.md) · [Contributing](../CONTRIBUTING.md)

This pass reconciles the unfinished first rollout and aligns eight shared files: validator, regression tests, contributor guide, AGENTS.md, BRANDING.md, .editorconfig, PR template and package CI. Original Quality workflows remain separate; package CI runs on Linux, Windows and macOS with Python 3.12.

## Review corrections

Activation-name validation counts duplicate plain/quoted top-level name keys before interpreting their values, including duplicate values with comments or unsupported scalar forms. Quotes must match; valid inline comments remain supported. The package contract supports a simple name scalar, not general YAML evaluation.

Ordinary Markdown link destinations are separated from optional titles and angle delimiters, while fenced/inline code examples are excluded. The scan remains limited to the four named guides and is not a complete Markdown, reference-link, HTML or anchor linter. This scope is explicit in the shared contributor guide.

Repository/install-name matching rejects a doubled -skill suffix while preserving the ledger's ai-usage-ledger key. Required base configuration is explicitly declared in each applicable manifest; config-generator alone does not force INI on future implementations. The common suite includes symlink-loop and escape regressions, required-file failures and corrupt PNG chunk checks. PNG pixel/decompression validation remains outside the structural contract.

The new matrix exposed a POSIX-only library-test assertion. It was corrected to compare the platform-native, shell-quoted destination without weakening the Windows job. Library audit normalizes only line endings, handles errors per checkout, and preserves the default exclusion of private members. PowerShell plans use literal quoting and reject control characters.

## Maintenance

```bash
python -m unittest discover -s tests -p 'test_package_*.py' -v
python scripts/validate_package.py
python scripts/validate_quality.py
python scripts/skill_library.py audit --workspace ./skills
```

The common suite uses parameterized negative and positive cases. The hub additionally tests catalog membership, install plans, shared-file drift and PowerShell behavior. Keep specialist onboarding commands tied to actual entry points, particularly ledger.py init/run and the independently consented scheduling operation.

These notes do not establish merge status or a registry release. Verify actual PR results and exact tested heads. Private sources/assets remain private, no live services are exercised by structural checks, and visual/factual review remains separate.

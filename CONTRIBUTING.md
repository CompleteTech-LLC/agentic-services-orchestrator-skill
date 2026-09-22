# Contributing to CompleteTech LLC Skills

[Start here](ONBOARDING.md) · [Branding and handoffs](BRANDING.md) · [Maintainer instructions](AGENTS.md) · [Specialist instructions](SKILL.md)

## Compatibility

Keep each skill independently usable. Preserve activation keys, root generator CLIs, templates, runtime dependencies, consent and approval gates. The ledger's standard-library core and neutral branding are intentional differences, not gaps to remove.

## Verification

From a full checkout using Python 3.12, the package CI baseline:

```bash
python -m unittest discover -s tests -p 'test_package_*.py' -v
python scripts/validate_package.py
```

Also run the existing quality and regression commands in [README.md](README.md). Package checks are read-only and do not execute specialist generators. They validate metadata, required files, local documentation links and PNG chunk integrity, not decoded artwork or document truth. Do not weaken original Quality checks to obtain a green result.

## Coordinated changes

Keep `skill-package.json`, onboarding and actual entry points synchronized. Shared validator, tests, CI, maintainer instructions and branding guidance must match the orchestrator's shared-file audit. Use focused PRs and report exact checks, failures and limitations. Respect branch protection, review requirements and changed heads.

Use synthetic fixtures and new output paths instead of overwriting committed previews. Never commit secrets, personal logs, real account mappings, client documents or unapproved quotes. Code remains under [LICENSE](LICENSE); branding remains under [BRAND_ASSETS.md](BRAND_ASSETS.md). Do not redistribute private assets or fonts. Registry releases and repository visibility changes require separate authorization.

# Contributing to CompleteTech LLC Skills

[Start here](ONBOARDING.md) · [Agent instructions](SKILL.md) · [Brand asset policy](BRAND_ASSETS.md)

## Scope and compatibility

Keep each skill independently usable. Preserve its skill key, CLI entry points, specialist templates, approval gates and documented network boundaries. The usage ledger retains its standard-library runtime; generator skills retain their root `generate_*.py` entry points. Do not move these solely to make directory trees identical.

Use a focused branch and PR. Describe the affected skill, user-visible change, compatibility impact, tests and any unverified behavior. Do not bypass branch protection, required review or failed checks.

## Package checks

From a full GitHub checkout, with Python 3.12 (the CI baseline):

```bash
python -m unittest discover -s tests -p test_package_contract.py -v
python scripts/validate_package.py
```

The package contract is standard-library-only and read-only: it checks metadata, navigation, local paths and the existing logo. It does not execute generators or certify document content. Also run this repository's existing quality and regression commands documented in [README.md](README.md). Where present, `scripts/validate_quality.py` remains an independent gate; do not remove or weaken it to pass package validation.

## Documentation and branding

Keep [ONBOARDING.md](ONBOARDING.md), `skill-package.json` and the actual entry points synchronized. Use **CompleteTech LLC Skills** for the family navigation and the existing `assets/logo.png`; do not substitute unrelated artwork. Keep outputs and temporary experiments under `output/` or a temporary directory, not over committed previews.

Code, templates and documentation retain their existing [MIT license](LICENSE). Names, logos, seals and other brand assets remain subject to [BRAND_ASSETS.md](BRAND_ASSETS.md); this package work grants no additional rights. Do not copy private assets or redistribute bundled fonts as part of a public package update.

## Evidence and privacy

Use synthetic fixtures. Never commit credentials, completion keys, personal logs, client documents, private account mappings or unapproved quotes. A successful render is not legal approval, payment authorization, verified attendance, security signoff, client acceptance or permission to publish/send.

Shared contract changes should be coordinated through the orchestrator's skill-library catalog and applied consistently to the affected siblings. `schema_version` versions the package contract, not a ClawHub release. Registry publication and repository visibility changes require separate explicit authorization.

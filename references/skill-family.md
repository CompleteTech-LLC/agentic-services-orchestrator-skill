# CompleteTech LLC Skills

A coordinated library of independently usable skills. This repository is the navigation, routing and maintenance hub; it does not replace specialist implementations or grant approval across their boundaries.

[Start here](../ONBOARDING.md) · [Branding and handoffs](../BRANDING.md) · [Maintainer instructions](../AGENTS.md) · [Catalog](skill-library.json) · [Second-pass notes](alignment-pass2.md)

## Choose the specialist

| Repository | Responsibility | Access |
|---|---|---|
| [ai-usage-ledger-skill](https://github.com/CompleteTech-LLC/ai-usage-ledger-skill) | Usage evidence and estimates; activation key `ai-usage-ledger` | Public |
| [agentic-services-orchestrator-skill](https://github.com/CompleteTech-LLC/agentic-services-orchestrator-skill) | Route work and preserve approval-aware state | Public |
| [agentic-discovery-skill](https://github.com/CompleteTech-LLC/agentic-discovery-skill) | Intake, readiness, scope and requirements | Public |
| [agentic-email-skill](https://github.com/CompleteTech-LLC/agentic-email-skill) | Draft message copy and sequences, without sending | Public |
| [agentic-proposal-skill](https://github.com/CompleteTech-LLC/agentic-proposal-skill) | Proposals, SOWs and pilot recommendations | Public |
| [agentic-contract-skill](https://github.com/CompleteTech-LLC/agentic-contract-skill) | Agreement packages from approved terms | Public |
| [agentic-invoice-skill](https://github.com/CompleteTech-LLC/agentic-invoice-skill) | Billing drafts from verified commercial facts | Public |
| [agentic-delivery-skill](https://github.com/CompleteTech-LLC/agentic-delivery-skill) | Kickoff, execution, evaluation, launch and handoff | Public |
| [agentic-security-review-skill](https://github.com/CompleteTech-LLC/agentic-security-review-skill) | Findings, controls and applicable launch blockers | Public |
| [agentic-customer-success-skill](https://github.com/CompleteTech-LLC/agentic-customer-success-skill) | Account health, renewal and expansion | Public |
| [agentic-case-study-skill](https://github.com/CompleteTech-LLC/agentic-case-study-skill) | Evidence-backed proof with explicit permission for use | Public |
| [agentic-envelope-skill](https://github.com/CompleteTech-LLC/agentic-envelope-skill) | Addressed envelopes and delivery packaging | Public |
| [agentic-certificate-skill](https://github.com/CompleteTech-LLC/agentic-certificate-skill) | Attendance certificates | Private; optional; existing access required |

Other activation keys match their repository names. Private selection does not grant access or change visibility. No private assets are copied into this public catalog.

## Installation planning

```bash
python scripts/skill_library.py list
python scripts/skill_library.py plan --destination ./skills
```

For PowerShell:

```powershell
python scripts/skill_library.py plan --shell powershell --destination ./skills
```

These commands list metadata or print quoted installation commands; they do not create directories, clone, install dependencies, execute skills or load credentials. Review the output and retain only the needed specialists. Use each skill's ONBOARDING.md and your agent product's documented discovery directory.

Plans follow current default branches, not a pinned or atomic suite release. Record reviewed commit SHAs for controlled deployment. Existing non-empty destinations are not updated by a clone plan. `--include-private` only selects the optional certificate member for an already-authorized operator; never embed tokens in commands.

## Offline audit

```bash
python scripts/skill_library.py audit --workspace ./skills
```

The audit validates each local checkout and its catalog identity, then compares eight shared text files against this hub. It normalizes platform line endings only; real content drift, missing files, unsafe paths and workspace escapes fail. It reads sibling files without importing or executing their code, and reports errors across the selected members. Add `--include-private` only when that authorized private checkout is already present.

| Shared path | Responsibility |
|---|---|
| `scripts/validate_package.py` | Read-only schema, file, navigation, guide-link and PNG-chunk checks |
| `tests/test_package_contract.py` | Synthetic common regressions, including malformed metadata and unsafe paths |
| `CONTRIBUTING.md` | Verification, compatibility, evidence and privacy expectations |
| `AGENTS.md` | Maintainer-agent instructions and specialist boundaries |
| `BRANDING.md` | Approved identity, starter palette and downstream handoffs |
| `.editorconfig` | UTF-8, LF and Python indentation defaults |
| `.github/PULL_REQUEST_TEMPLATE.md` | Change, evidence, boundary and family-consistency reporting |
| `.github/workflows/package-contract.yml` | Linux, Windows and macOS package CI on Python 3.12 |

README navigation is common, while ONBOARDING.md and skill-package.json remain specialist-specific. Required base configurations and other demonstration dependencies belong in `example_inputs`; implementation kind alone does not imply one configuration format. The existing certificate, contract and envelope manifests explicitly list their base INI files.

## Specialist behavior and approvals

Catalog renderers retain their scripts and templates; config generators retain their root CLIs; the hub retains adapters and `project_state`; the ledger retains its standard-library core, neutral branding and explicit source/retention choices. Match presentation through approved settings and local assets, not by replacing every output with one layout.

Use the existing [workflow schema](workflow-definition-schema.yaml) and [services adapter](completetech-services-workflow.yaml). Preserve evidence, artifact versions, approved identity, confidentiality, audience, approval owners/statuses, blockers and next specialist at handoff. The ledger supplies estimates, not authority to bill. Anonymization is not publication consent, and a rendered certificate is not evidence of attendance.

## Verification boundaries

```bash
python -m unittest discover -s tests -p 'test_package_*.py' -v
python scripts/validate_package.py
python scripts/validate_quality.py
```

The first two need only Python. The original Quality gate has its own documented dependencies and remains mandatory alongside package checks. The guide-link scan covers ordinary inline destinations in ONBOARDING.md, CONTRIBUTING.md, BRANDING.md and AGENTS.md, not all Markdown, HTML or anchors. PNG validation covers bounded chunks/CRCs, not decompression or artwork. Run the specialist checks and inspect actual generated outputs separately. Schema 1 is a checkout contract, not a registry version or release certification.

# CompleteTech LLC Skills

A coordinated library of independently usable skills, with consistent branding, onboarding and a machine-checkable package contract. This repository is the navigation and routing hub, not a replacement for specialist implementations.

[Start with the orchestrator](../ONBOARDING.md) · [Operating instructions](../SKILL.md) · [Machine-readable catalog](skill-library.json)

## Choose a skill

| Repository | Responsibility | Access |
|---|---|---|
| [ai-usage-ledger-skill](https://github.com/CompleteTech-LLC/ai-usage-ledger-skill) | Usage evidence, attribution and API-equivalent costs; install key `ai-usage-ledger` | Public |
| [agentic-services-orchestrator-skill](https://github.com/CompleteTech-LLC/agentic-services-orchestrator-skill) | Route work, preserve state and enforce the applicable approval boundaries | Public |
| [agentic-discovery-skill](https://github.com/CompleteTech-LLC/agentic-discovery-skill) | Intake, readiness, scope and requirements | Public |
| [agentic-email-skill](https://github.com/CompleteTech-LLC/agentic-email-skill) | Draft message copy and sequences, without sending | Public |
| [agentic-proposal-skill](https://github.com/CompleteTech-LLC/agentic-proposal-skill) | Proposals, SOWs and pilot recommendations | Public |
| [agentic-contract-skill](https://github.com/CompleteTech-LLC/agentic-contract-skill) | Agreement packages from approved terms | Public |
| [agentic-invoice-skill](https://github.com/CompleteTech-LLC/agentic-invoice-skill) | Billing drafts from verified commercial facts | Public |
| [agentic-delivery-skill](https://github.com/CompleteTech-LLC/agentic-delivery-skill) | Kickoff, execution, evaluation, launch and handoff | Public |
| [agentic-security-review-skill](https://github.com/CompleteTech-LLC/agentic-security-review-skill) | Security findings, controls and relevant launch blockers | Public |
| [agentic-customer-success-skill](https://github.com/CompleteTech-LLC/agentic-customer-success-skill) | Account health, commitments, renewal and expansion | Public |
| [agentic-case-study-skill](https://github.com/CompleteTech-LLC/agentic-case-study-skill) | Evidence-backed proof assets with explicit approval for use | Public |
| [agentic-envelope-skill](https://github.com/CompleteTech-LLC/agentic-envelope-skill) | Addressed envelopes, attachment manifests and packaging | Public |
| [agentic-certificate-skill](https://github.com/CompleteTech-LLC/agentic-certificate-skill) | Attendance certificates | Private; optional; existing authorization required |

All other install keys match their repository names. The private skill is excluded from default plans and audits; including it does not grant access, change visibility or authorize publication. No private assets are included in the public catalog.

## Installation plan, not automatic installation

From a full orchestrator checkout:

```bash
python scripts/skill_library.py list
python scripts/skill_library.py plan --destination ./skills
```

`plan` prints quoted commands for a POSIX shell; it does not create directories, clone repositories, install dependencies, load credentials or execute skills. Review the plan, retain only the skills needed, and run approved commands yourself. On Windows, use the listed HTTPS repository URLs with Git and the explicit install-directory names, or review the POSIX plan in Git Bash/WSL.

The plan follows each repository's current default branch. It is not a pinned, reproducible or atomic suite release. For a controlled deployment, record and review each selected commit SHA before use. Existing destination directories are not updated by the plan: Git refuses to clone over non-empty checkouts. Update those separately after reviewing their changes.

Use `--include-private` only for an operator already authorized to access the certificate repository. Never add tokens to generated commands, commit credentials or copy private sources into public repositories. Each skill's `ONBOARDING.md` covers its own environment setup and safe first run. Install full directories in the location documented by the chosen agent product; the catalog does not assume one product's global directory.

## Offline cross-repository audit

Place sibling checkouts under one directory using their skill keys (or repository names for existing workspaces), then run:

```bash
python scripts/skill_library.py audit --workspace ./skills
```

The audit validates each manifest, declared local entry points/examples, frontmatter name, README navigation and brand asset. It also checks that `scripts/validate_package.py`, `tests/test_package_contract.py`, `CONTRIBUTING.md` and `.github/workflows/package-contract.yml` exactly match the copies in this orchestrator checkout. Missing skills and drift fail explicitly. It does not fetch remote repositories or execute their code. Add `--include-private` to audit an already-authorized local certificate checkout.

## Shared package contract, schema 1

| Path | Purpose |
|---|---|
| `README.md` | Existing specialist overview plus consistent family navigation and logo reference |
| `ONBOARDING.md` | Environment setup, install key, safe first result, branding, permissions and troubleshooting |
| `CONTRIBUTING.md` | Shared compatibility, evidence, privacy, branding and PR expectations |
| `skill-package.json` | Family identity, install key, repository, implementation kind, entry points, example inputs and network mode |
| `scripts/validate_package.py` | Standard-library, read-only checkout validation |
| `tests/test_package_contract.py` | Synthetic regression tests for malformed metadata, paths, links and assets |
| `.github/workflows/package-contract.yml` | Dedicated, least-privilege CI; existing quality workflows remain independent |

This adds a package layer to the [existing shell standard](skill-layout-standardization.md). It does not require identical implementations: catalog renderers remain in `scripts/`, config generators retain root `generate_*.py` CLIs, the orchestrator keeps workflow adapters, and the ledger keeps its own storage/pipeline and standard-library runtime. The package schema version is not a registry release version.

## Consistent presentation without weakening safeguards

Use **CompleteTech LLC Skills** in family navigation and reuse the existing `assets/logo.png`. Retain specialist document types and layouts: a one-page invoice is not a proposal cover, and an envelope is not an attendance certificate. The ledger's neutral-by-default branding remains intentional; choose its CompleteTech preset explicitly rather than forcing it on personal reports. Existing [brand asset restrictions](../BRAND_ASSETS.md) remain unchanged.

Use bundled demonstrations for onboarding, write new outputs under `output/` or the documented synthetic-test output directory, and preserve committed previews. A successful render or structural check is not a review of visual quality or truth. Do not invent metrics, approvals, attendance, financial facts, legal authority or client permission.

## Lifecycle handoffs

A typical engagement moves from discovery to proposal, contract, invoice, delivery, customer success and approved proof. Email and envelope skills support communication and packaging; security review participates only where the relevant risk gate requires it. The ledger supplies evidence, not authority to bill, and certificates remain a distinct attendance workflow.

Use the existing [workflow schema](workflow-definition-schema.yaml) and [CompleteTech services adapter](completetech-services-workflow.yaml). Preserve verified facts, source artifacts, applicable approval owners/statuses, blockers and open questions in `project_state`. Installing the library does not enable external actions or confer approval across specialist boundaries.

## Verification and maintenance

```bash
python -m unittest discover -s tests -p 'test_package_*.py' -v
python scripts/validate_package.py
python scripts/validate_quality.py
```

The first two commands need only Python; the existing full quality validator has additional documented dependencies. Review coordinated PRs independently, respect required checks/reviews, then audit the resulting sibling checkouts for drift. Do not publish registry releases or change private/public visibility as an implicit part of a structural update.

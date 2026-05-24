---
name: agentic-services-orchestrator-skill
description: >-
  Coordinate the CompleteTech LLC agentic services skill library across discovery, proposal, contract, delivery, customer success, invoice, certificate, case study, email, envelope, and security-review workflows. Use when Codex needs to identify lifecycle stage, route to specialist skills, pass project context, manage handoffs, prevent duplicate work, weave in supporting plugins, and preserve one coherent client/project state.
version: 1.0.0
metadata:
  openclaw:
    skillKey: agentic-services-orchestrator-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-services-orchestrator-skill
---

# Agentic Services Orchestrator Skill

## Purpose

Coordinate the CompleteTech LLC agentic services lifecycle. The orchestrator owns workflow state, routing, sequencing, dependency tracking, handoff contracts, missing-info handling, approval gates, and plugin-weaving. Specialist skills own their artifacts.

For the complete architecture, per-skill responsibility matrix, handoff schema, plugin-weaving model, deduplication guidance, and example multi-skill workflows, load `references/orchestration-architecture.md`.

## Lifecycle Model

Discovery -> Proposal -> Contract -> Delivery -> Customer Success.

Supporting outputs: Invoice, Certificate, Case Study, Email, Envelope.

Overlay/gate: Security Review.

## Routing Logic

1. Classify intent: create artifact, route work, continue workflow, package/send outputs, review risk, collect missing facts, or approve a transition.
2. Identify lifecycle stage and current state from explicit user context, existing artifacts, or prior handoff notes.
3. Select the earliest missing lifecycle artifact unless the user requests a specific support output.
4. Invoke security review before sensitive data use, new tools/integrations, external actions, production launch, payment/billing actions, credential changes, or public proof.
5. Use email only for message drafting and sequences. Use envelope only for packaging, recipients, attachments, filenames, metadata, and delivery-readiness.
6. Return a handoff package with artifact paths, decisions, unresolved questions, blockers, approvals, next owner, and next recommended skill.

## Skill Invocation Rules

- `agentic-discovery-skill`: fact finding, workflow maps, readiness, success criteria, risk/excluded-use checks, and proposal handoff briefs.
- `agentic-proposal-skill`: buyer-facing scope, SOWs, pilot recommendations, evaluation plans, roadmaps, and change-order proposals.
- `agentic-contract-skill`: agreement content and contract package generation from approved commercial facts.
- `agentic-delivery-skill`: execution, kickoff, project controls, evaluation, launch readiness, handoff, runbooks, and closeout after approval.
- `agentic-customer-success-skill`: relationship state, contact routing, account health, renewals, expansion, escalations, and advocacy planning.
- `agentic-invoice-skill`: invoice-event selection, invoice drafts, billing documents, credits, receipts, retainers, and payment requests.
- `agentic-certificate-skill`: certificate PDF generation from verified recipient and course/workshop facts.
- `agentic-case-study-skill`: verified and approved proof, testimonials, public stories, quote approval, anonymization, and proof libraries.
- `agentic-email-skill`: outbound/inbound message copy, sequences, cover notes, follow-ups, and approval request drafts.
- `agentic-envelope-skill`: addressed envelopes, delivery packages, attachments, recipient metadata, filenames, and send/readiness checklists.
- `agentic-security-review-skill`: confidentiality, sensitive data, permissions, compliance/risk, approval gates, launch blockers, and escalation.

## Boundary Rules

- The orchestrator owns routing and state; specialist skills do not own lifecycle orchestration.
- Email drafts must not replace proposals, invoices, contracts, delivery records, customer records, security reviews, certificates, or proof.
- Envelope packaging must not create contract, invoice, certificate, proposal, delivery, proof, or email content.
- Discovery outputs are not final proposals, contracts, invoices, delivery plans, security signoffs, or public proof.
- Proposal scope must use verified discovery or user-provided facts; use `TBD` for missing scope, proof, pricing, outcomes, or approvals.
- Contract and invoice artifacts must not invent legal, pricing, tax, payment, client, authority, signature, or approval facts.
- Delivery artifacts must stay inside approved scope; route new scope to proposal or change-order work first.
- Security review does not equal legal approval, formal compliance certification, or external penetration testing unless verified evidence is provided.
- Customer success notes are internal/account artifacts, not public proof.
- Case studies, testimonials, quotes, and named references require verified approval.
- Certificates require verified recipient and course/workshop facts; they are not delivery acceptance or public proof.

## Context-Passing Schema

Use this shape when handing work between skills:

```yaml
project_state:
  client: TBD
  workflow: TBD
  lifecycle_stage: discovery|proposal|contract|delivery|customer_success
  requested_outcome: TBD
  source_artifacts: []
  known_facts: {}
  missing_info: []
  blockers: []
  approvals:
    commercial: unknown
    legal_or_contract: unknown
    security: unknown
    external_send: unknown
    public_proof: unknown
  security_flags: []
  next_skill: TBD
  downstream_handoff: TBD
```

## Common Workflows

1. Lead to scoped proposal: discovery -> email recap -> proposal -> security review if sensitive data/tools are involved.
2. Proposal to signed kickoff: proposal -> contract -> invoice -> envelope package -> email cover note -> delivery after approval.
3. Delivery launch readiness: delivery -> security review -> approval gate -> email status/update -> customer success handoff.
4. Post-launch support: delivery support record -> customer success health/renewal -> invoice for retainer/overage if approved.
5. Proof creation: delivery evidence -> customer success approver/timing -> case study -> security/anonymization gate -> email approval request.
6. Training certificate: certificate -> envelope package if mailed -> email delivery message if sent digitally.

## Operating Pattern

1. Identify the lifecycle stage and current missing artifact.
2. Route to the most specific specialist skill.
3. Pass a compact `project_state` object plus artifact-specific inputs.
4. Preserve facts, assumptions, blockers, approvals, and open questions during handoff.
5. Use `TBD` for unknowns instead of filling gaps.
6. Stop at the appropriate approval gate before public use, legal commitment, invoice issuance, production launch, external communication, packaging/sending, or proof publication.
7. After a specialist returns output, update `project_state` and name the next skill or blocker.

## Unresolved Questions

- If the library becomes one package, should repeated renderer logic and shared assets move into common helpers?
- Should `agentic-case-study-skill` be renamed to `agentic-proof-skill`?
- Should sending, invoice issuance, and public proof publication get a dedicated approval workflow file shared by email, envelope, invoice, and case study?

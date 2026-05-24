# CompleteTech Agentic Services Orchestration Architecture

## 1. Executive Summary

The library should operate as one service-delivery system. `agentic-services-orchestrator-skill` owns lifecycle state, routing, sequencing, handoff contracts, missing-info handling, approval gates, duplicate-work prevention, and plugin selection. Specialist skills perform bounded business functions. Support skills provide reusable communication, packaging, proof, billing, certificate, and risk-review capabilities.

The lifecycle is Discovery -> Proposal -> Contract -> Delivery -> Customer Success. Invoice, Certificate, Case Study, Email, and Envelope are supporting outputs. Security Review is an overlay/gate that can interrupt any stage.

## 2. Final Architecture

- Orchestrator: central workflow manager, state owner, router, gatekeeper, and handoff normalizer.
- Lifecycle skills: discovery, proposal, contract, delivery, customer success.
- Support skills: invoice, certificate, case study, email, envelope.
- Overlay/gate skill: security review.
- Plugins: used by the orchestrator or support skills only when they materially complete a workflow, such as GitHub for repo work, Gmail for mailbox context, Canva for branded design, spreadsheet tools for tabular client/project tracking, and document/PDF generators for artifacts.

## 3. Skill Responsibility Matrix

| Skill | Purpose | Orchestrator invokes when | Required inputs | Optional inputs | Outputs | Upstream | Downstream | Shared skills/plugins | Gates | Must not own | Centralize/remove |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| discovery | Convert opportunity into verified workflow facts. | New lead, unclear scope, readiness unknown, proposal facts missing. | client/workflow, stakeholders, pain, systems, goals, constraints. | budget, timeline, data/tool notes, examples. | intake, workflow map, readiness, success criteria, proposal handoff. | email, customer request. | proposal, security, customer success. | email for recap; security for risk. | sensitive data, excluded use, unclear approval path. | Final proposal, contract, invoice, launch approval. | lifecycle routing, security gates, email copy. |
| proposal | Create buyer-facing commercial scope. | Discovery facts are sufficient for pilot/SOW/proposal/change order. | verified facts, scope, deliverables, acceptance criteria, price/terms if known. | proof snippets, roadmap, risk plan. | proposal, SOW, evaluation plan, assumptions/exclusions. | discovery, customer success, delivery change request. | contract, invoice, email, envelope. | security for risk; case study for approved proof only. | claims, regulated use, unapproved proof, pricing authority. | Legal terms, billing doc, delivery execution. | orchestration, email cover text, envelope packaging. |
| contract | Generate agreement package from approved terms. | Proposal/SOW is approved or user requests contract artifact. | legal parties, signatories, effective date, services summary, fees, terms source. | watermark/branding, output paths. | contract PDF/Markdown package. | proposal, human-approved terms. | invoice, envelope, email, delivery. | envelope for mailing; email for cover note. | legal approval, signature authority, unknown terms. | Scope negotiation, invoice issuance, packaging policy. | envelope ownership and lifecycle routing. |
| delivery | Produce execution artifacts after approval. | Work is approved and needs kickoff, status, evaluation, launch, handoff, support, closeout. | approved scope, timeline, owners, access needs, deliverables, acceptance criteria. | risks, logs, test examples, support terms. | project plan, trackers, status, evaluation, runbook, closeout. | contract/proposal, security. | customer success, invoice, case study, email. | security for launch; email for updates. | production launch, external actions, access changes. | Commercial scope, account renewal, public proof. | security gates, email drafts, billing. |
| customer success | Maintain relationship/account state. | Post-contact, active delivery, support, renewal, expansion, risk, advocacy. | client, contacts, routing, commitments, success criteria, account stage. | health score, renewal date, support items. | account profile, contact map, health score, QBR, renewal/expansion brief. | discovery, delivery, support. | case study, invoice, proposal, email. | email for outreach; case study for advocacy. | contact approval, escalation, billing/security concerns. | Delivery execution, public proof content. | orchestration state, email copy. |
| invoice | Draft billing documents. | Deposit, milestone, retainer, change order, support, credit, receipt, or payment request is needed. | client/provider, amount, terms, line items, invoice number, due date, contract/SOW ref. | taxes, discounts, payments, notes. | invoice, credit memo, receipt, payment request. | proposal, contract, delivery, customer success. | envelope, email, customer success. | envelope for mailing; email for send note. | billing approval, tax/accounting review, payment instructions. | Pricing rationale, legal terms, collections strategy. | lifecycle routing, email copy, envelope packaging. |
| certificate | Generate attendance certificate PDFs. | Verified training/workshop attendance certificate is requested. | recipient name, recipient email, certificate title. | issue date override, signatory, config override. | certificate PDF/path. | delivery/training record, user-provided facts. | envelope, email, customer success. | envelope/email for delivery. | identity/attendance verification. | Delivery acceptance, public proof. | routing, packaging, email. |
| case study | Package approved proof. | Outcomes are verified and proof/testimonial/story is requested. | approved facts, outcomes, attribution permission, confidentiality constraints. | quotes, metrics, proof snippets, channel. | case study, testimonial draft, proof library, anonymization checklist. | delivery, customer success. | email, proposal proof reuse, website/social. | security for anonymization; email for approval/share. | client approval, confidentiality, public proof. | Account management, delivery evidence creation. | security/anonymization gates, email drafts. |
| email | Draft communication. | Any workflow needs outbound/inbound copy, cover note, sequence, approval ask, or follow-up. | audience, stage, artifact summary, CTA, tone, verified recipient/routing. | prior messages, objections, proof snippets. | email draft/sequence. | any lifecycle/support skill. | envelope/send workflow, human approval. | Gmail only with explicit mailbox need. | external send approval, recipient verification. | Proposals, contracts, invoices, delivery records, proof facts. | artifact routing, packaging, state. |
| envelope | Package and address deliverables. | Outputs need mailing, attachment inventory, filename/recipient metadata, delivery-readiness, or envelope PDF. | sender, recipient, mailing address or recipient metadata, artifacts/attachments. | attention line, postage text, return-address toggle, filenames. | envelope PDF, package manifest, delivery-readiness checklist. | contract, invoice, certificate, proposal, case study. | email/send, human approval, archive. | email for digital send; security for sensitive package. | recipient verification, sensitive attachments. | Business content of artifacts or email copy. | artifact generation, lifecycle routing. |
| security review | Review risk and approvals. | Sensitive data, credentials, tools, integrations, external actions, billing, launch, public proof, incident, or permission changes appear. | workflow, data classes, tools, permissions, external actions, approval gates, logs, rollback. | provider/model config, retention, dependencies. | risk intake, permission inventory, launch blocker list, signoff memo. | any stage. | orchestrator decision, delivery, email, envelope, customer success. | technical/security plugins as needed. | launch, external send/action, public proof, credentials. | Legal certification, formal pen test claim. | duplicated risk gates in other skills. |

## 4. Orchestrator Routing and Handoff Model

Routing order:

1. Honor explicit user target if it is safe and has required inputs.
2. If target is unclear, infer lifecycle stage from artifacts and requested outcome.
3. Select the earliest missing lifecycle artifact before downstream outputs.
4. Add support skills only for a concrete job: email for copy, envelope for packaging, invoice for billing, certificate for attendance, case study for proof.
5. Run security review before risky transitions.
6. Return next skill, output artifacts, blockers, and missing facts.

Handoff schema:

```yaml
project_state:
  client: TBD
  workflow: TBD
  lifecycle_stage: discovery|proposal|contract|delivery|customer_success
  intent: create|revise|package|send|review|approve|handoff
  source_artifacts: []
  known_facts: {}
  assumptions: []
  missing_info: []
  blockers: []
  approvals:
    commercial: unknown
    legal_or_contract: unknown
    security: unknown
    external_send: unknown
    public_proof: unknown
  security_flags: []
  generated_outputs: []
  next_skill: TBD
  next_action: TBD
```

Failure modes:

- Missing required facts: ask targeted questions or insert `TBD`.
- Conflicting facts: stop and ask for source of truth.
- Unsafe request: route to security review or require human approval.
- Duplicate artifact: revise the existing artifact instead of creating a parallel one.
- Downstream request before upstream approval: produce a draft only and record the blocker.

## 5. Plugin-Weaving Model

- GitHub: code/repo artifacts, issue/PR workflows, CI evidence, commit/push tasks.
- Gmail: mailbox context, thread summaries, reply drafting, recipient history; sending requires explicit approval.
- Canva: branded presentations or visual assets that exceed Markdown/PDF templates.
- Spreadsheet tools: client trackers, invoice tables, account health matrices, opportunity lists.
- Local generators: use each skill renderer/generator before hand-rolling repeatable documents.

The orchestrator chooses plugins, but specialist skills may request them through the handoff when their artifact needs external context or production output.

## 6. Deduplication and Centralization Recommendations

- Move lifecycle routing, sequencing, state, and duplicate prevention to the orchestrator.
- Move email subject/body/CTA/sequences to email.
- Move recipients, filenames, attachment manifests, delivery-readiness, and physical mailing envelope PDFs to envelope.
- Move sensitive data, confidentiality, compliance, tool permission, external action, launch, and public-proof gates to security review.
- Keep lifecycle skills focused on business artifacts and handoff facts.
- Keep renderer/template selection inside each specialist; centralize only the handoff contract.
- Avoid repeating full boundary paragraphs in every skill; each skill should state only local ownership and what it returns.

## 7. Final Cleaned Instruction Set: Orchestrator

Use the orchestrator when a request spans more than one skill or stage. It must:

1. Build or update `project_state`.
2. Classify stage, intent, missing facts, approvals, blockers, and risk flags.
3. Route to the right lifecycle skill or support skill.
4. Pass only relevant context to each specialist.
5. Convert outputs into downstream inputs.
6. Prevent duplicate work by checking existing artifacts first.
7. Invoke security review at every risk gate.
8. Use email only for communication copy and envelope only for packaging/delivery-readiness.
9. Return artifact paths, decisions, missing info, approval status, and next step.

## 8. Final Cleaned Instruction Outlines

- Discovery: collect verified pre-sale workflow facts; output proposal-ready handoff and risk flags; do not draft final commercial/legal artifacts.
- Proposal: turn verified facts into buyer-facing scope; output contract/invoice/delivery-ready scope; do not own legal terms, billing, or send packaging.
- Contract: generate agreement package from approved terms; output contract artifacts; do not own commercial negotiation or delivery packaging policy.
- Delivery: manage approved execution artifacts; output evidence, acceptance, handoff, and support records; do not own commercial expansion or public proof.
- Customer Success: maintain relationship/account state; output contact maps, health, renewal, escalation, and advocacy plans; do not own implementation artifacts.
- Invoice: create billing documents from approved commercial triggers; output invoice artifacts; do not own accounting/tax/legal decisions.
- Certificate: generate attendance certificates from verified recipient/course facts; output certificate PDF paths; do not own proof or delivery acceptance.
- Case Study: package verified approved outcomes; output proof assets and approval/anonymization notes; do not invent metrics or public permission.
- Email: draft messages and sequences from supplied artifacts; output copy; do not create the underlying business artifact or send without approval.
- Envelope: package artifacts for delivery; output envelope PDFs, attachment manifests, filenames, recipients, and readiness notes; do not author artifact content.
- Security Review: assess risk, permissions, sensitive data, external actions, and launch/proof gates; output blockers/signoff/residual risks; do not claim formal certification.

## 9. Example Workflows

Lead to proposal:

1. Orchestrator builds project state and routes to discovery.
2. Discovery returns workflow facts, missing scope, and risk flags.
3. Security review runs if data/tool risk exists.
4. Proposal drafts a pilot or SOW.
5. Email drafts recap or proposal cover note.
6. Envelope packages the proposal only if mailing or attachment manifest is needed.

Proposal to kickoff:

1. Proposal returns approved scope and assumptions.
2. Contract generates agreement package.
3. Invoice drafts deposit request from approved terms.
4. Envelope prepares contract/invoice package and recipient metadata.
5. Email drafts send/follow-up copy.
6. Delivery starts only after approval/signature/payment gate status is clear.

Launch readiness:

1. Delivery produces evaluation, launch checklist, runbook, and handoff.
2. Security review checks permissions, external actions, rollback, logs, and blockers.
3. Orchestrator stops for approval if blockers remain.
4. Email drafts client status update.
5. Customer success receives account/support state.

Proof after closeout:

1. Delivery provides verified evidence.
2. Customer success identifies approver and timing.
3. Case study drafts anonymized or named proof based on approval status.
4. Security review checks confidentiality.
5. Email drafts approval request or publication note.

Training certificate:

1. Certificate generates PDF from verified recipient/course facts.
2. Envelope packages physical mailing if needed.
3. Email drafts digital delivery note if needed.

## 10. Open Questions

- Should `agentic-case-study-skill` be renamed `agentic-proof-skill` to match its broader proof-asset role?
- Should approval gates be stored in a shared machine-readable file, such as `references/approval-gates.yaml`, for reuse by email, envelope, invoice, case study, and security review?
- Should shared renderer conventions move to a common package once the library is published as one installable bundle?
- Should envelope become the sole source for all physical mailing output, while contract keeps only its embedded legacy `--envelope-out` generator option for backward compatibility?

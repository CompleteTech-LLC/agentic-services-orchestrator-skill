# Engagement Orchestration Overview

Worked example of the CompleteTech LLC agentic services lifecycle for one engagement: the Northwind Trading Co. Customer Support Email Triage Agent pilot. The orchestrator owns state, routing, sequencing, handoffs, and approval gates; specialist skills own their artifacts.

## 1. Lifecycle Routing

| Stage | Skill | Artifact produced | Gate before next |
|---|---|---|---|
| Discovery | discovery | Requirements brief (DISC-2026-0117) | Facts verified |
| Proposal | proposal | Pilot proposal (PRO-2026-0188) | Commercial approval |
| Contract | contract | Agreement (ADSA-2026-0142) | Signature + deposit |
| Delivery | delivery | Launch readiness checklist | Security signoff |
| Overlay | security review | Signoff memo (SEC-2026-0090) | Conditional GO |
| Support | customer success | Health scorecard & QBR | Renewal decision |
| Proof | case study | Named case study (approved) | Public-use approval |
| Billing | invoice | Milestone invoice (INV-2026-0461) | Billing approval |
| Comms | email | Outbound sequence | Verified recipient |
| Packaging | envelope | #10 addressed envelope | Approved to send |

## 2. Example project_state Handoff

> The orchestrator passes a compact state object between skills and uses TBD for unknowns rather than inventing facts.

| Field | Value |
|---|---|
| client | Northwind Trading Co. |
| workflow | Support email triage agent |
| lifecycle_stage | delivery |
| approvals.commercial | approved |
| approvals.security | conditional (R-03 open) |
| approvals.external_send | unknown |
| next_skill | security-review → delivery |
| next_action | Close R-03, then run acceptance demo |

## 3. Routing Logic

- Select the earliest missing lifecycle artifact unless the user requests a specific support output.
- Invoke security review before launch, new tools, external actions, billing, or public proof.
- Use email only for message copy; use envelope only for packaging and delivery-readiness.
- Return a handoff package: artifact paths, decisions, open questions, blockers, approvals, next owner.

## 4. Boundary Reminders

- Discovery facts are not a proposal; a proposal is not a contract; a contract does not authorize launch.
- Case studies, testimonials, and named references require verified client approval.
- Certificates require verified recipient/course facts and are not delivery acceptance or public proof.

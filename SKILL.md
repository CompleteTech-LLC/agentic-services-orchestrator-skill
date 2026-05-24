---
name: agentic-services-orchestrator-skill
description: Coordinate the CompleteTech LLC agentic services skill library across discovery, email, proposal, contract, invoice, delivery, security review, customer success, case study, and certificate workflows. Use when Codex needs to choose, sequence, or hand off between multiple agentic specialist skills without replacing their detailed instructions.
---

# Agentic Services Orchestrator Skill

## Purpose

Coordinate the CompleteTech LLC agentic services lifecycle. Use this skill to choose, sequence, and hand off between specialist skills. Do not replace specialist templates, skip their guardrails, or invent missing facts.

## Routing Guide

- Discovery/scoping, workflow facts, readiness, success criteria, and proposal handoff: `agentic-discovery-skill`.
- Outreach, follow-up, cover notes, delivery updates, retention, referral, and win-back message copy: `agentic-email-skill`.
- Proposal, SOW, commercial scope, pilot, change order, evaluation/risk plan, roadmap, or buyer approval summary: `agentic-proposal-skill`.
- Agreement package, contract PDF, filled Markdown, branded contract output, or envelope: `agentic-contract-skill`.
- Invoice, deposit, payment, credit, refund, retainer, pass-through, receipt, or billing document: `agentic-invoice-skill`.
- Approved delivery execution, kickoff, project controls, evaluation, launch, support, handoff, runbook, or closeout: `agentic-delivery-skill`.
- Security, permissions, data, credentials, tool access, retrieval trust, external actions, launch risk, rollback, incident response, or signoff: `agentic-security-review-skill`.
- Account health, contact routing, follow-ups, renewal, expansion, escalation, advocacy planning, or at-risk recovery: `agentic-customer-success-skill`.
- Approved proof, case study, testimonial, public story, quote approval, anonymization, press, award, or portfolio asset: `agentic-case-study-skill`.
- Attendance certificate, course/workshop completion certificate, recipient certificate PDF, or certificate ID generation: `agentic-certificate-skill`.

When more than one route applies, choose the earliest missing lifecycle artifact first, then hand off to the next specialist skill.

## Boundary Rules

- Email drafts must not replace proposals, invoices, contracts, delivery records, customer records, security reviews, certificates, or proof.
- Discovery outputs are not final proposals, contracts, invoices, delivery plans, security signoffs, or public proof.
- Proposal scope must use verified discovery or user-provided facts; use `TBD` for missing scope, proof, pricing, outcomes, or approvals.
- Contract and invoice artifacts must not invent legal, pricing, tax, payment, client, authority, signature, or approval facts.
- Delivery artifacts must stay inside approved scope; route new scope to proposal or change-order work first.
- Security review does not equal legal approval, formal compliance certification, or external penetration testing unless verified evidence is provided.
- Customer success notes are internal/account artifacts, not public proof.
- Case studies, testimonials, quotes, and named references require verified approval.
- Certificates require verified recipient and course/workshop facts; they are not delivery acceptance or public proof.

## Common Workflows

1. Lead to scoped proposal: `agentic-discovery-skill` for facts and fit, `agentic-email-skill` for outreach/recaps, then `agentic-proposal-skill` for proposal or SOW.
2. Proposal to signed kickoff: `agentic-proposal-skill` for final scope, `agentic-contract-skill` for agreement, `agentic-invoice-skill` for deposit or kickoff billing, `agentic-email-skill` for send/follow-up, then `agentic-delivery-skill` after approval.
3. Delivery launch readiness: `agentic-delivery-skill` for execution, evaluation, acceptance, runbooks, support, and handoff; `agentic-security-review-skill` for permissions, data, tool actions, launch blockers, rollback, and signoff; `agentic-email-skill` for client updates.
4. Post-launch support and account management: `agentic-delivery-skill` for support/handoff records, `agentic-customer-success-skill` for account health and renewal/expansion, and `agentic-invoice-skill` for support, retainer, overage, or renewal billing.
5. Post-project proof or testimonial creation: `agentic-delivery-skill` for evidence, `agentic-customer-success-skill` for approver timing, `agentic-case-study-skill` for approved proof, and `agentic-email-skill` for approval/share messages.
6. Training or workshop certificate generation: `agentic-certificate-skill` for the certificate PDF when facts are verified; `agentic-email-skill` only for the delivery message.

## Operating Pattern

1. Identify the lifecycle stage and current missing artifact.
2. Route to the most specific specialist skill.
3. Preserve facts and open questions during handoff.
4. Use `TBD` for unknowns instead of filling gaps.
5. Stop at the appropriate approval gate before public use, legal commitment, invoice issuance, production launch, external communication, or proof publication.

## Unresolved Questions

- If the library becomes one package, should repeated renderer logic and shared assets move into common helpers?
- Should `agentic-case-study-skill` be renamed to `agentic-proof-skill`?
- Should sending, invoice issuance, and public proof publication get a separate approval workflow?

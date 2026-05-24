# Agentic Services Orchestrator Skill

A CompleteTech LLC Codex skill for routing multi-stage agentic services work across the specialist skill library.

## Workflow Diagram

```mermaid
flowchart LR
  A[Request or client stage] --> B{Primary need}
  B -->|Scope| C[Discovery]
  B -->|Sell| D[Email and proposal]
  B -->|Approve| E[Contract and invoice]
  B -->|Build| F[Delivery and security]
  B -->|Operate| G[Customer success]
  B -->|Prove or certify| H[Case study or certificate]
  C --> D --> E --> F --> G --> H
  classDef source fill:#eef6ff,stroke:#3778c2,color:#102a43;
  classDef gate fill:#fff7e6,stroke:#c97a12,color:#3d2600;
  classDef output fill:#eefaf0,stroke:#2f8f46,color:#12351d;
  class A source;
  class B gate;
  class C,D,E,F,G,H output;
```

## What It Does

- Chooses and sequences the right CompleteTech agentic specialist skill.
- Keeps specialist boundaries clear across discovery, email, proposal, contract, invoice, delivery, security review, customer success, proof, and certificate work.
- Preserves facts and open questions during handoff.
- Stops at approval gates before public use, legal commitment, invoice issuance, production launch, external communication, or proof publication.

## Contents

- `SKILL.md` - orchestration instructions, routing guide, boundary rules, and common multi-skill workflows.
- `agents/openai.yaml` - OpenAI agent metadata.

## Brand Notes

Use a direct, practical, low-hype tone. The orchestrator coordinates the lifecycle; it does not replace specialist templates or invent missing facts.

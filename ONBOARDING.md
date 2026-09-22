# Start here: agentic-services-orchestrator-skill

<p align="center"><img src="assets/logo.png" alt="CompleteTech LLC logo" width="260"></p>

**CompleteTech LLC Skills** — Lifecycle routing and approval-aware handoffs.

[Overview](README.md) · [Agent instructions](SKILL.md) · [Contributing](CONTRIBUTING.md) · [Skill library](https://github.com/CompleteTech-LLC/agentic-services-orchestrator-skill/blob/main/references/skill-family.md)

## 1. Choose the right skill

This is an `orchestrator`. Its install/activation key is **`agentic-services-orchestrator-skill`**. Use the orchestrator when work spans multiple specialists; install only the specialists the engagement needs. Install the complete skill directory, including `SKILL.md`, references, scripts and assets, in the directory supported by your agent. Do not install only the Markdown file. Keep this skill separate from its siblings.

## 2. Get a full checkout and prepare Python

Python 3.12 is the shared CI baseline. Git is needed only for cloning. The full GitHub checkout includes the existing brand assets; text-only registry packages can omit binary logos/previews and are not the target of the checkout validator.

```bash
git clone https://github.com/CompleteTech-LLC/agentic-services-orchestrator-skill.git agentic-services-orchestrator-skill
cd agentic-services-orchestrator-skill
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate_package.py
```

On Windows PowerShell, create the environment with `py -3 -m venv .venv`, then use `.\.venv\Scripts\python.exe` instead of `python` in subsequent commands. Activation is optional; do not change machine execution policy for this skill. For an existing checkout, skip `git clone` and start at environment setup.

## 3. Run a safe demonstration

Run from the skill root. The commands below use bundled synthetic/example inputs, not client data. They can replace an earlier demonstration at the same output path; choose a new filename when retaining prior output.

```bash
python scripts/render_pdf.py --markdown assets/examples/example.md --out output/onboarding-demo.pdf --logo assets/logo.png --title "Orchestration demonstration"
```

The bundled orchestration overview renders to `output/onboarding-demo.pdf`. For actual routing, load `references/completetech-services-workflow.yaml` and follow `SKILL.md`; generating this PDF does not execute a workflow or approve a transition.

Open the generated output and inspect page breaks, tables, logo, text and any remaining placeholders. Package validation checks structure; it does not certify visual quality or factual correctness. Committed previews in `assets/examples/` are references, not destinations for your first run.

## 4. Use the skill with your agent

Read [SKILL.md](SKILL.md), select `agentic-services-orchestrator-skill` using your agent's skill activation mechanism, and provide verified inputs, the requested artifact, destination and required approval owners. Agent discovery paths differ by product; follow that product's installation documentation rather than assuming one global path. Do not grant broader permissions simply because multiple skills are installed together.

## Branding and handoff

Use the existing CompleteTech LLC logo and the practical, evidence-led voice described in [README.md](README.md). The code license does not grant logo, seal or signature rights: follow [BRAND_ASSETS.md](BRAND_ASSETS.md). Do not replace or republish private artwork or fonts.

For a multi-skill handoff, preserve the source facts, artifact paths, approval owner/status, blockers and next specialist in the orchestrator's existing `project_state` schema. Do not treat a generated artifact, anonymization or successful check as permission to send, publish, bill, sign, award or launch.

## Safety and permissions

The documented generation workflow is local. Installation may contact GitHub and package indexes, but generation does not send messages, move money, publish documents, grant approval or install background services. Review the specialist boundaries in [SKILL.md](SKILL.md) before using real inputs.

## Troubleshooting and verification

A missing module usually means the active interpreter differs from the one used for `pip`; use `python -m pip` in the same environment and this repository's `requirements.txt`. Missing logos or references usually indicate a partial/text-only installation or the wrong working directory; use a full checkout and run from its root. Do not download replacement branding from unrelated sources.

```bash
python -m unittest discover -s tests -p test_package_contract.py -v
python scripts/validate_package.py
```

These checks use the standard library and do not execute the listed generators, scan accounts, contact services or install schedules. Follow [CONTRIBUTING.md](CONTRIBUTING.md) and the repository's existing quality instructions for the additional runtime, rendering, parser and diagram checks.

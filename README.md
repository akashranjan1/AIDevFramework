# Salesforce Delivery Orchestrator

Provider-neutral automation for taking a Jira story through a governed Salesforce delivery lifecycle: discovery, planning, branch creation, implementation, validation, deployment, commit, and pull request.

It is agent-agnostic. Claude, Codex, Copilot, or a human can use the same task contract and skills; the orchestrator owns deterministic integrations and approval gates.

## Quick start

Prerequisites: Python 3.11+, `git`; optionally `sf`, `gh`, and Jira credentials.

```powershell
Copy-Item config\orchestrator.example.yaml config\orchestrator.yaml
python -m sfdc_orchestrator.cli plan ABC-123
python -m sfdc_orchestrator.cli run ABC-123 --approve plan --approve branch
```

The example config is dry-run enabled. Set `safety.dry_run: false` only after configuring named Salesforce orgs and CI/PR integrations. Store secrets in environment variables or a secret manager, never the config.

## Operating model

```text
Jira story -> discovery -> plan [approval] -> branch [approval]
          -> agent implementation -> quality -> validate/deploy -> commit -> PR [approval]
```

Each run creates evidence in `.delivery-runs/`. A stage cannot proceed without its dependencies and required approval.

## Agent integration

Give any agent the task contract emitted by `plan` and point it at `skills/`. It may edit code and propose changes, but must return structured evidence following `schemas/agent-result.schema.json`. The orchestrator then invokes deterministic checks and integration commands.

## SDLC controls to add in CI

- Jira acceptance criteria, dependency, release target, and estimate traceability.
- Apex and LWC tests, linting/formatting, static analysis, secret/dependency scanning.
- Validate-only Salesforce deployments before production; documented rollback strategy.
- Code owners, linked Jira issue, test/deployment evidence, and release notes on every PR.
- Separate, auditable production approval and deployment from development automation.

## Layout

```text
config/             workflow policy and integration templates
skills/             portable instructions for any coding agent
schemas/            machine-readable agent contract
sfdc_orchestrator/  Python CLI and pipeline engine
tests/              policy tests
```

To extend it, add stages in YAML or replace command templates with real adapters for Jira, Git, Salesforce DX, GitHub, Azure DevOps, or your CI system.

# Adoption path

## 1. Establish the delivery contract

Copy the example configuration, define branch naming and environments, and add the three skills to the instruction mechanism of each supported agent. Every agent receives the same Jira-derived task contract and must emit the same result JSON. This keeps agent choice separate from release controls.

## 2. Connect non-production first

Replace the command templates with your approved Jira CLI/API wrapper, `sf` commands, and PR provider. Configure a least-privilege integration identity for each sandbox. Do not give development agents production credentials.

## 3. Put deterministic quality gates in CI

Run Salesforce Code Analyzer, PMD/ESLint, Prettier, Jest, Apex tests, secret scanning, dependency scanning, and metadata diff checks. CI should call `sf project deploy validate` against the appropriate integration org and publish logs as build artifacts.

## 4. Separate production promotion

Production must be an independently approved release pipeline. It should deploy a previously validated artifact, create a Salesforce deployment record, update the change ticket, verify smoke tests, and retain rollback instructions. The coding agent must not self-approve this transition.

## Governance checklist

- Use protected branches, CODEOWNERS, required reviews, and signed/verified CI checks.
- Enforce Jira issue linkage and acceptance-criteria-to-test traceability.
- Capture prompts, tool/command outputs, changed files, test results, deployment IDs, and approvals as immutable evidence.
- Redact secrets and customer data from prompts, logs, and agent context.
- Establish policy for destructive metadata changes, data migrations, permission-set changes, and managed-package upgrades.
- Add evaluation stories to measure agent plan quality, test quality, review findings, and deployment success before wider rollout.

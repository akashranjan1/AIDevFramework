# AI Dev Framework repository instructions

This repository combines a provider-neutral delivery framework with a Salesforce DX project.

- Salesforce source and metadata belong in `Akash-Dev/`; the project file is `Akash-Dev/sfdx-project.json`.
- Reviewable Jira plans belong in `thoughts/plan/<ISSUE-KEY>.md`.
- Jira Cloud story snapshots are retrieved with `scripts/get_jira_story.py` and saved temporarily under `thoughts/source/`; this directory is ignored by Git because issue contents can be sensitive.
- Repository skills are in `.agents/skills/`. Use `$create-plan` before `$implement-plan`.
- Do not fabricate Jira content. Retrieve it through an authorized integration or ask for its text.
- Never deploy, commit, push, open a pull request, or modify Jira unless the user explicitly requests that exact stage.
- Never put credentials, access tokens, auth URLs, customer data, or secrets in Git, plans, prompts, or logs.

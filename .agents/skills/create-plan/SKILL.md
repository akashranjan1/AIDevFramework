---
name: create-plan
description: Create a review-only Salesforce delivery plan for a Jira story. Use when asked to plan a story, analyze a Jira issue, or create an implementation plan. Never modify Salesforce metadata, source code, Git branches, or deployments.
---

# Create a Salesforce story plan

The remaining user prompt must contain a Jira issue key (for example `ABCD-123`), a Jira URL, or the complete story text.

1. Read the supplied story. First, use an existing `thoughts/source/<ISSUE-KEY>.json` snapshot when it exists. Otherwise, for Jira Cloud, when `JIRA_BASE_URL`, `JIRA_EMAIL`, and `JIRA_API_TOKEN` are available in the terminal environment, retrieve it with `py -3 scripts/get_jira_story.py <ISSUE-KEY> --output thoughts/source/<ISSUE-KEY>.json`. Read the saved snapshot, including its ADF description, linked issues, and attachments. If credentials or Jira access are unavailable, say so plainly and request the story text; never invent issue contents.
2. Inspect the repository. Salesforce source is under `Akash-Dev/`, especially `Akash-Dev/force-app/main/default`. Read relevant tests, metadata, and repository conventions before proposing a solution.
3. Create exactly one Markdown plan at `thoughts/plan/<ISSUE-KEY>.md`. Create the directory when required. Replace unsafe path characters in the issue key with `-`.
4. Use this structure: story summary; source/evidence; assumptions and open questions; acceptance-criteria traceability; affected files and metadata; ordered implementation steps; Apex/LWC/Flow test cases; permissions/sharing/security considerations; validation and deployment steps; rollback approach; risks/dependencies; review checklist.
5. Make the plan specific enough for another developer to implement, but do not make implementation changes, create a branch, change an org, deploy, commit, push, or create a pull request.
6. End the response with the plan path and ask the user to review it. State that implementation begins only after the user explicitly invokes `$implement-plan <ISSUE-KEY>` or otherwise approves the named plan.

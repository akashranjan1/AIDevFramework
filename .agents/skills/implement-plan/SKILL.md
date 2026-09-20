---
name: implement-plan
description: Implement an explicitly approved Salesforce story plan created by create-plan. Use only when the user names an existing reviewed plan and asks to implement it; do not deploy, commit, push, or create a pull request unless separately requested.
---

# Implement an approved Salesforce story plan

1. Locate `thoughts/plan/<ISSUE-KEY>.md`. If it is absent, ambiguous, or not explicitly approved by the current user request, stop and ask for the plan or approval.
2. Re-read the plan and inspect the relevant source under `Akash-Dev/` before changing files. Treat the plan as the scope boundary; call out any necessary divergence before acting.
3. Check `git status`. Create a feature branch using the configured naming convention only if the user has asked for branch creation or has explicitly approved implementation with branch creation.
4. Implement source and metadata changes in `Akash-Dev/`. Use bulk-safe Apex, explicit sharing and CRUD/FLS decisions, least-privilege permissions, and deterministic tests. Avoid `SeeAllData=true` unless justified in the plan.
5. Add or update focused tests. Run safe local checks available in the repository and report their results.
6. Do not deploy to Salesforce, commit, push, create a pull request, alter Jira, or mark the story complete unless the user separately requests that stage.
7. Report changed files, tests/results, remaining risks, and the exact suggested next command: `$validate-story <ISSUE-KEY>`.

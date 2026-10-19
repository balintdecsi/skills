---
name: gh-cli
description: Enforces authenticated gh CLI workflows over unauthenticated curl, wget, or WebFetch patterns. Use for GitHub repositories, URLs, API access, raw files, pull requests, issues, releases, or private content. Do not use for non-GitHub services or when plain local Git fully solves the task.
---

# gh-cli

## Guidance

Prefer the authenticated `gh` CLI over raw HTTP fetches for GitHub content. In particular:

- Prefer `gh repo view`, `gh pr view`, `gh pr list`, `gh issue view`, and `gh api` over unauthenticated `curl` or `wget`.
- Prefer cloning a repository and reading files locally over fetching `raw.githubusercontent.com` blobs directly.
- Avoid using GitHub API `/contents/` endpoints as a substitute for cloning and reading repository files.
- Before sending private or unpublished content to a new repository, explain the transfer and get user approval.
- Treat requested routine issue and pull-request edits as authorized, but confirm destructive, repository-level, or irreversible actions.

Examples:

```sh
gh repo view owner/repo
gh pr view 123 --repo owner/repo
gh api repos/owner/repo/pulls
```

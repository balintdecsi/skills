---
name: find-skills
description: Helps users discover and, with permission, install agent skills when they ask to find a skill, ask whether a skill exists, or want to extend agent capabilities. Check installed and repository-local skills first; search the external ecosystem only when no suitable local skill exists. Do not divert an ordinary task into skill discovery merely because the user asks “how do I do X?”.
---

# Find Skills

This skill helps discover skills from the open ecosystem and install one after
the user approves the verified source and scope.

## What is the Skills CLI?

The Skills CLI (`npx skills@1.7.2`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools. The examples below pin the reviewed CLI version; verify the source and release before updating that pin.

**Key commands:**

- `npx skills@1.7.2 find [query]` - Search for skills interactively or by keyword
- `npx skills@1.7.2 add <package>` - Install a skill from GitHub or other sources
- `npx skills@1.7.2 check` - Check for skill updates
- `npx skills@1.7.2 update` - Update all installed skills

**Browse skills at:** https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need

When the user asks to discover or install a skill, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Check Local Skills, Then the Leaderboard

Inspect installed and repository-local skills first. Use a matching local skill instead of searching for or installing a duplicate. If none fits, check the [skills.sh leaderboard](https://skills.sh/) before running a CLI search. The leaderboard ranks skills by total installs, surfacing popular options.

For example, top skills for web development include:
- `vercel-labs/agent-skills` — React, Next.js, web design (100K+ installs each)
- `anthropics/skills` — Frontend design, document processing (100K+ installs)

### Step 3: Search for Skills

If the leaderboard doesn't cover the user's need, run the find command:

```bash
npx skills@1.7.2 find [query]
```

Search only with generic capability terms. Do not send private repository
content, personal data, unpublished product details, or secrets in the query.

For example:

- "Find a React performance skill" → `npx skills@1.7.2 find react performance`
- "Is there a changelog skill?" → `npx skills@1.7.2 find changelog`

### Step 4: Verify Quality Before Recommending

**Do not recommend a skill based solely on search results.** Always verify:

1. **Install count** — Prefer skills with 1K+ installs. Be cautious with anything under 100.
2. **Source reputation** — Official sources (`vercel-labs`, `anthropics`, `microsoft`) are more trustworthy than unknown authors.
3. **GitHub stars** — Check the source repository. A skill from a repo with <100 stars should be treated with skepticism.

### Step 5: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. The install count and source
3. The install command they can run
4. A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.
(185K installs)

To install it:
npx skills@1.7.2 add vercel-labs/agent-skills@react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### Step 6: Offer to Install

If the user explicitly chooses to proceed after reviewing the source and requested scope, install the skill project-locally by default with the verified Skills CLI:

```bash
npx skills@1.7.2 add <owner/repo@skill> -y
```

Use `-g` only when the user separately approves a global (user-level) install:

```bash
npx skills@1.7.2 add <owner/repo@skill> -g -y
```

The `-y` flag skips the CLI's confirmation prompt only after the user has approved the source and scope.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills@1.7.2 init`

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills@1.7.2 init my-xyz-skill
```

# skills

This repository contains my global [Agent Skills](https://agentskills.io) that I use across different projects.

## What are Agent Skills?

From [agentskills.io](https://agentskills.io):

> **Why Agent Skills?**
> Agents are increasingly capable, but often don't have the context they need to do real work reliably. Skills solve this by packaging procedural knowledge and company-, team-, and user-specific context into portable, version-controlled folders that agents load on demand. This gives agents:

## How I use these skills

- **Global skills** – I place skills in `~/.agents/` so they are accessible to agents in any project on my machine.
- **Project-specific skills** – I place skills in the project root's `.agents/` folder when I want to add context that is only relevant to that particular project.

## Adding skills

When I create skills myself (e.g. for data science and machine learning best practices and industry standards), I reference the public repositories where I take inspiration from in the skill markdown.

When I want to add an already existing skill from the web, I use the [skills.sh](https://skills.sh) tool:

```bash
npx skills add
```

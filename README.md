# skills

This repository contains global [Agent Skills](https://agentskills.io) for analytics, data science, and machine learning workflows.

## What are Agent Skills?

From [agentskills.io](https://agentskills.io):

> **Why Agent Skills?**
> Agents are increasingly capable, but often don't have the context they need to do real work reliably. Skills solve this by packaging procedural knowledge and company-, team-, and user-specific context into portable, version-controlled folders that agents load on demand. This gives agents:

## How to use these skills

- **Global skills** — place skills in `~/.agents/skills/` (or symlink this repo there) so agents can load them in any project.
- **Project-specific skills** — place skills in the project root's `.agents/` folder when context applies only to that project.

## Installing external skills

When adding an existing skill from the web, use the [skills.sh](https://skills.sh) tool:

```bash
npx skills add
```

## Skills in this repo

| Skill | Focus |
|---|---|
| [analytics-project-setup](analytics-project-setup/) | Repo scaffolding, environments, notebooks, pre-commit |
| [code-review](code-review/) | AI code review with CodeRabbit |
| [data-warehousing](data-warehousing/) | Bronze / silver / gold pipelines, validations-as-code |
| [designing-analytics-projects](designing-analytics-projects/) | Analytics Project Brief (scoping before code) |
| [find-skills](find-skills/) | Discover and install skills from the ecosystem |
| [gh-cli](gh-cli/) | Authenticated GitHub CLI workflows |
| [ml-modeling](ml-modeling/) | scikit-learn pipelines, CV, model comparison |
| [statistical-modeling](statistical-modeling/) | OLS / logistic regression, intervals, stargazer |
| [time-series-forecasting](time-series-forecasting/) | Temporal splits, ARIMA, AutoGluon, backtesting |
| [uv](uv/) | Python environments and dependency management with uv |

## Sources and attribution

Many skills distill patterns from CEU MSBA coursework, open course repositories, and standard references. Each skill's `SKILL.md` links to the relevant notebooks and files; the table below is the index.

| Skill | Course / source | Instructor / author | Repository |
|---|---|---|---|
| **data-warehousing** | ECBS5294 — Introduction to Data Science: Working with Data | Eduardo Ariño de la Rubia | [earino/ECBS5294](https://github.com/earino/ECBS5294) |
| **designing-analytics-projects** | ECBS5228A — Designing Analytics Projects | Eduardo Arino de la Rubia | [earino/designing-analytics-projects](https://github.com/earino/designing-analytics-projects) |
| **ml-modeling** | ECBS5233 — Data Science 3: Machine Learning Concepts and Tools | János Divényi | [divenyijanos/ceu-ml](https://github.com/divenyijanos/ceu-ml) |
| **ml-modeling**, **statistical-modeling** | *Data Analysis for Business, Economics, and Policy* (case studies, datasets) | Gábor Békés, Gábor Kézdi | [gabors-data-analysis/da_case_studies](https://github.com/gabors-data-analysis/da_case_studies), [gabors-data-analysis/da_data_repo](https://github.com/gabors-data-analysis/da_data_repo) |
| **ml-modeling** | AI Engineering, Modern Data Platforms (light context) | Zoltán C. Tóth | [zoltanctoth/ceu-ai-engineering-class](https://github.com/zoltanctoth/ceu-ai-engineering-class), [zoltanctoth/ceu-modern-data-platforms](https://github.com/zoltanctoth/ceu-modern-data-platforms) |
| **statistical-modeling** | Coding 2 — MS in Business Analytics (regression intro) | CEU Coding 2 course | *(private coursework)* |
| **time-series-forecasting** | Time Series Forecasting (CEU) | Francesca Conselvan | [francescaconselvan/time_series_forecasting](https://github.com/francescaconselvan/time_series_forecasting) |
| **analytics-project-setup** | Industry project structure | — | [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/), [ageron/handson-ml3](https://github.com/ageron/handson-ml3) |

When a skill cites a file path (e.g. `notebooks/class5_bike_share_demand.ipynb`), it refers to that path inside the repository listed above unless another URL is given explicitly.

# skills

This repository contains global [Agent Skills](https://agentskills.io) for software engineering, analytics, data science, product work, compliance, and command-line workflows.

## What are Agent Skills?

From [agentskills.io](https://agentskills.io):

> **Why Agent Skills?**
> Agents are increasingly capable, but often don't have the context they need to do real work reliably. Skills solve this by packaging procedural knowledge and company-, team-, and user-specific context into portable, version-controlled folders that agents load on demand.

## How to use these skills

- **Global skills** — place skills in `~/.agents/skills/` (or symlink this repo there) so agents can load them in any project.
- **Project-specific skills** — place skills in the project root's `.agents/` folder when context applies only to that project.

## Installing external skills

When adding an existing skill from the web, use the [skills.sh](https://skills.sh) tool:

```bash
npx skills@1.7.2 add
```

## Sources and attribution

Some skills distill patterns from CEU MSBA coursework, open course repositories, and standard references. Skills derived from external material link to their relevant sources; original and CLI-focused skills may not have a course source. The table below records external attribution where applicable.

| Skill | Course / source | Instructor / author | Repository | Upstream licence |
|---|---|---|---|---|
| **data-warehousing** | ECBS5294 — Introduction to Data Science: Working with Data | Eduardo Ariño de la Rubia | [earino/ECBS5294](https://github.com/earino/ECBS5294) | CC BY 4.0 (course materials; `data/` excluded) |
| **designing-analytics-projects** | ECBS5228A — Designing Analytics Projects | Eduardo Ariño de la Rubia | [earino/designing-analytics-projects](https://github.com/earino/designing-analytics-projects) | CC BY 4.0 |
| **ml-modeling** | ECBS5233 — Data Science 3: Machine Learning Concepts and Tools | János Divényi | [divenyijanos/ceu-ml](https://github.com/divenyijanos/ceu-ml) | None declared — used with the author's permission |
| **ml-modeling**, **statistical-modeling** | *Data Analysis for Business, Economics, and Policy* (case studies, datasets) | Gábor Békés, Gábor Kézdi | [gabors-data-analysis/da_case_studies](https://github.com/gabors-data-analysis/da_case_studies), [da_data_repo on OSF](https://osf.io/3u5em/) | MIT (case studies) |
| **ml-modeling** | AI Engineering, Modern Data Platforms (light context) | Zoltán C. Tóth | [zoltanctoth/ceu-ai-engineering-class](https://github.com/zoltanctoth/ceu-ai-engineering-class), [zoltanctoth/ceu-modern-data-platforms](https://github.com/zoltanctoth/ceu-modern-data-platforms) | CC BY-NC 4.0 / BSD-3 |
| **statistical-modeling** | Coding 2 — MS in Business Analytics (regression intro) | CEU Coding 2 course | *(private coursework)* | — |
| **time-series-forecasting** | Time Series Forecasting (CEU) | Francesca Conselvan | [francescaconselvan/time_series_forecasting](https://github.com/francescaconselvan/time_series_forecasting) | None declared |
| **geospatial-ds** | Geospatial Data Science (CEU MSBA) | Milán Janosov | *(course notebooks shared privately; not redistributed)* — [The New Science of Maps](https://www.thenewscienceofmaps.com/) | — (attribution approved by the instructor) |
| **product-discovery** | Entrepreneurship and Innovation (CEU MSBA, 2026) | Andrea Kozma | *(course slides shared privately; not redistributed)* — plus published frameworks (Ries, Blank, Sarasvathy, Aulet, Christensen, Fitzpatrick) | — (ideas and structure only; no copied expression) |
| **analytics-project-setup** | Industry project structure | — | [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/), [ageron/handson-ml3](https://github.com/ageron/handson-ml3) | MIT / Apache-2.0 |

When a skill cites a file path (e.g. `notebooks/class5_bike_share_demand.ipynb`), it refers to that path inside the repository listed above unless another URL is given explicitly.

## Licence

Everything written for this repository is released under the [MIT License](LICENSE).

A few files derive from, or cite, third-party material under other licences (MIT,
Apache-2.0, BSD-3-Clause, CC BY 4.0, CC BY-NC 4.0, GPL-2.0+, and some course
repositories with no licence declared). Those are itemised, with their upstream
notices and current permission status, in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

Course material is credited to its instructors as attribution, not endorsement.

# Third-Party Notices

The skills in this repository are original writing by the repository author and are
released under the [MIT License](LICENSE). A small number of files derive from, or
cite, third-party material. Those are listed here with their upstream licence.

Last verified: 2026-09-02.

## Derived material (code adapted from an upstream source)

| File | Upstream | Upstream licence | Status |
|---|---|---|---|
| `statistical-modeling/snippets/spline_helpers.py` | [da_case_studies `ch00-tech-prep/da_helper_functions.py`](https://github.com/gabors-data-analysis/da_case_studies/blob/master/ch00-tech-prep/da_helper_functions.py) | MIT — Copyright (c) 2021 Gabors Data Analysis | Permitted. Upstream notice retained in the file header, as MIT requires. |
| `ml-modeling/snippets/result_collector.py` | [ceu-ml `class5_bike_share_demand.ipynb`](https://github.com/divenyijanos/ceu-ml/blob/2026/notebooks/class5_bike_share_demand.ipynb) | **None declared** (all rights reserved by default) | ⚠️ **Permission is being sought; not yet obtained.** If declined, replace with an independent implementation. |
| `designing-analytics-projects/SKILL.md` | [earino/designing-analytics-projects](https://github.com/earino/designing-analytics-projects) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — Copyright (c) 2026 Eduardo Arino de la Rubia | Permitted with attribution. Licence named in the skill; no endorsement implied. |

## Cited-only sources (ideas, structure and pointers — no copied expression)

Facts, methods and workflow patterns are not protected by copyright; these are
credited as a matter of courtesy and scholarly practice, not licence obligation.

| Source | Licence | Used by |
|---|---|---|
| [earino/ECBS5294](https://github.com/earino/ECBS5294) | None declared | `data-warehousing` |
| [francescaconselvan/time_series_forecasting](https://github.com/francescaconselvan/time_series_forecasting) | None declared | `time-series-forecasting` |
| [divenyijanos/ceu-ml](https://github.com/divenyijanos/ceu-ml) | None declared | `ml-modeling` (workflow discussion) |
| [gabors-data-analysis/da_case_studies](https://github.com/gabors-data-analysis/da_case_studies) | MIT | `ml-modeling`, `statistical-modeling` |
| [da_data_repo](https://osf.io/3u5em/) (OSF; the GitHub mirror is gone) | None declared | `ml-modeling`, `statistical-modeling` |
| [zoltanctoth/ceu-ai-engineering-class](https://github.com/zoltanctoth/ceu-ai-engineering-class) | CC BY-NC 4.0 | `ml-modeling` (pointer only — the NonCommercial term does not attach, as nothing is derived from it) |
| [zoltanctoth/ceu-modern-data-platforms](https://github.com/zoltanctoth/ceu-modern-data-platforms) | BSD-3-Clause | `ml-modeling` (pointer only) |
| [ageron/handson-ml3](https://github.com/ageron/handson-ml3) | Apache-2.0 | `analytics-project-setup` |
| [dbt-labs/jaffle-shop-classic](https://github.com/dbt-labs/jaffle-shop-classic) | Apache-2.0 (archived) | `data-warehousing` |
| [StatsReporting/stargazer](https://github.com/StatsReporting/stargazer) | GPL-2.0-or-later | `statistical-modeling` — the library is *imported* by example code, never copied, so its copyleft does not extend to this repository |
| [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) | MIT | `analytics-project-setup` |
| CEU MSBA Geospatial Data Science course — Milán Janosov ([janosov.com](https://janosov.com)) | Course notebooks shared privately with enrolled students; **not redistributed here** | `geospatial-ds` — teaching approach only. Verified against the course notebooks: no prose overlap, and the only matching code lines are bare imports and single standard library calls. |

## Vendored licence

`notion-cli/LICENSE.md` reproduces the MIT licence of the Notion CLI
(Copyright (c) 2026 Notion Labs, Inc.), which the skill documents.

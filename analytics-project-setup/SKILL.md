---
name: analytics-project-setup
description: Technical setup skill for analytics and data science projects — repository scaffolding, folder structure (dev/prod split, data layers, numbered notebooks), environment management (uv, venv, dotenv), pre-commit hooks for notebook output clearing, branching and commit conventions, .gitignore patterns, AGENTS.md creation, database/storage I/O patterns, and production orchestration notebooks. Use when initialising a new analytics project, setting up a repo for a data science team, or creating an AGENTS.md file.
---

# Analytics Project Setup — Technical Guide

These are **codified best practices** for scaffolding, configuring, and maintaining analytics and data science project repositories. The patterns are distilled from production analytics experience and industry-standard practices from [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) and Géron's [*Hands-On Machine Learning*](https://github.com/ageron/handson-ml3).

They adapt to any cloud (GCP, AWS, Azure) or local stack.

## When to Use

Auto-apply when the task involves:

- Initialising a new analytics / data science project repository.
- Creating or updating folder structure for a modelling project.
- Setting up `.env`, `.gitignore`, or pre-commit hooks.
- Writing or reviewing `README.md` for an analytics project.
- Creating an `AGENTS.md` file for an analytics project.
- Starting a new repository with a proven analytics structure.
- Setting up environment management (virtual environments, requirements).
- Configuring branching strategy or commit conventions for a data team.
- Deploying notebooks to production (cloud or on-premise).

## The Canonical Folder Structure

Every project follows this layout. The `dev/` and `prod/` split is the single most important structural decision — it separates exploratory work from production-grade code.

```
├── data/                                    # Data (NOT in version control)
│   ├── external/                            # Third-party / lookup data
│   ├── interim/                             # Intermediate transforms
│   ├── processed/                           # Final, canonical datasets
│   │   ├── train_sample.csv
│   │   └── test_sample.csv
│   └── raw/                                 # Immutable original data dump
│
├── dev/                                     # Development workspace
│   ├── models/                              # Trained model artifacts (.pkl)
│   ├── notebooks/                           # Jupyter notebooks (numbered!)
│   │   ├── 01_features.ipynb
│   │   ├── 02_exploration.ipynb
│   │   ├── 03_preprocessing.ipynb
│   │   └── 04_modelling.ipynb
│   ├── sql/                                 # SQL queries for data generation
│   │   └── data_gen.sql
│   ├── src/                                 # Reusable Python modules
│   │   ├── __init__.py
│   │   ├── io.py                            # Data I/O helpers (DB, storage)
│   │   ├── explore.py                       # EDA utilities, plot helpers
│   │   └── datadrift_PSI.py                 # Data drift monitoring (PSI)
│   └── visualization/                       # Generated plots, figures
│
├── examples/                                # Reference notebooks & templates
│   ├── EDA_notebook.ipynb
│   ├── datadrift_PSI_example.ipynb
│   ├── preprocessing_notebook.ipynb
│   ├── environment_variable_example.ipynb
│   └── environment_variable_example.env
│
├── prod/                                    # Production workspace
│   ├── models/                              # Production model artifacts
│   ├── notebooks/                           # Production notebooks
│   │   └── project-process-control.ipynb    # Orchestrator notebook
│
├── .gitignore                               # Python + project-specific ignores
├── requirements.txt                         # Pinned dependencies
├── AGENTS.md                                # AI agent instructions (see below)
└── README.md                                # Project documentation
```

### Key Structural Rules

1. **Number notebooks by execution order:** `01_`, `02_`, `03_`, … This makes the workflow self-documenting.
2. **`dev/` is your sandbox, `prod/` is sacred.** Experimental code stays in `dev/`. Only reviewed, stable code moves to `prod/`.
3. **`data/` is never committed.** It lives in `.gitignore`. Data goes in cloud storage or is generated via SQL.
4. **`dev/visualization/` is never committed.** Plots are ephemeral outputs, regenerated from notebooks.
5. **`dev/src/` contains reusable modules** — import these in notebooks, don't copy-paste code between cells.
6. **`examples/` contains reference material** — EDA templates, environment setup examples, data drift examples.
7. **Keep runtime config minimal.** Start with environment variables and small Python config modules; add heavier config layers only when needed.

## Lightweight Configuration Pattern

Skip heavyweight config files at first. Use `.env` for secrets and a tiny Python module for paths and table names:

```python
# dev/src/config.py
from pathlib import Path

ROOT = Path(".")
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "dev" / "models"
SQL_DIR = ROOT / "dev" / "sql"
NOTEBOOK_ORDER = [
    "01_precheck.ipynb",
    "02_features.ipynb",
    "03_modelling.ipynb",
    "04_evaluation.ipynb",
]
```

Keep it simple until complexity justifies introducing a dedicated config file format.

## Repository Naming Convention

Use a consistent scheme so repos are discoverable:

```
<org>-<team>-<project_name>
```

- `<org>` — company/org code (e.g. `acme`).
- `<team>` — **kebab-case**, the team or department (e.g. `data-science`, `analytics`).
- `<project_name>` — **snake_case**, descriptive name (e.g. `churn_prediction`).

Examples:

- `acme-analytics-churn_prediction`
- `acme-data-science-demand_forecasting`

## Branching Strategy

**Never commit directly to `master` / `main`.** Use topic branches with these prefixes:

| Prefix | Purpose | Example |
|---|---|---|
| `data/` | Data collection tasks | `data/internal-stores-segment-1` |
| `analysis/` | Analysis work | `analysis/eda-customer-segments` |
| `model/` | Modelling tasks | `model/finetune-second-round` |
| `bugfix/` | Bug fixes | `bugfix/missing-polygon-manual-add` |
| `release/` | Production deployment | `release/v2-map-aesthetics` |

## Commit Message Conventions

- **Language:** English.
- **Tense:** Imperative (think: "This commit will _…_").
- **Style:** Capitalised, no trailing punctuation, 3–7 words.

Examples:

- `Add feature engineering notebook`
- `Solve duplication issue on table 420`
- `Include docs folder in gitignore`
- `Shortlist different tree-based models`

## Environment Management

### Recommended: `uv` (modern, fast)

For new projects, prefer `uv` (see the `uv` skill for details):

```bash
uv init
uv add pandas scikit-learn matplotlib numpy scipy
uv add --dev ipykernel jupyter nbconvert
```

### Legacy: `venv` + `requirements.txt`

The classic `venv` workflow still works fine:

```bash
python -m venv .venv
source .venv/bin/activate     # Linux/Mac
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### Standard analytics dependencies

```
ipykernel
scipy
numpy
matplotlib
pandas
scikit-learn
ydata-profiling
missingno
joblib
shap
```

Pin versions for production (`matplotlib==3.7.2`). Leave unpinned in dev for flexibility.

### Environment Variables with `dotenv`

For secrets (API keys, database credentials) that must **never** be committed:

```bash
pip install python-dotenv
```

Create `.env` in project root (already in `.gitignore`):

```
DB_PASSWORD=my_secret_password
API_KEY=abc123
```

Load in notebooks:

```python
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("DB_PASSWORD")
```

## Pre-commit Hook: Clearing Notebook Outputs

**Non-negotiable.** Notebook outputs bloat repos, leak data, and cause merge conflicts. Use a direct Git hook at `.git/hooks/pre-commit` (no extra hook framework):

```bash
cat > .git/hooks/pre-commit <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

# Clear outputs for staged notebooks only, then re-stage them.
staged_notebooks="$(git diff --cached --name-only --diff-filter=ACM -- '*.ipynb')"
[ -z "${staged_notebooks}" ] && exit 0

while IFS= read -r notebook; do
  [ -f "${notebook}" ] || continue
  jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace "${notebook}"
  git add "${notebook}"
done <<< "${staged_notebooks}"
EOF

chmod +x .git/hooks/pre-commit
```

This relies on the standard Jupyter/ipykernel environment (`jupyter`, `nbconvert`, `ipykernel`) already included in project dependencies.

## Git Configuration

When initializing a new repository, run:

```bash
# Make versioning case-sensitive (important for Python)
git config core.ignoreCase false

# Remove data/ and dev/visualization/ from git cache if they were in the template
git rm -r --cached data 2>/dev/null || true
git rm -r --cached dev/visualization 2>/dev/null || true
```

## The `.gitignore` Must-Haves

Beyond the standard Python gitignore template, always include:

```gitignore
# Project-specific
data/
dev/visualization/
images/

# Environment
.env
.venv/
venv/
pyvenv.cfg

# Jupyter
*.ipynb_checkpoints

# VS Code
.vscode/
```

## Production Orchestration Pattern

The `prod/notebooks/project-process-control.ipynb` pattern runs all production notebooks in sequence:

```python
from pathlib import Path

project_root = Path("/project_name")
notebooks = [
    "01_precheck.ipynb",
    "02_features.ipynb",
    "03_modelling.ipynb",
    "04_evaluation.ipynb",
]

for notebook in notebooks:
    file = project_root / notebook
    try:
        %run $file
        print(f"{notebook} is done")
    except Exception as e:
        print(f"Run of {notebook} stopped with error")
        print("The caught error is:")
        print(e)
        break
```

This ensures notebooks run in the defined order and fail fast on errors.

## Database / Storage I/O Patterns

Centralise data access through parameterised SQL files and a small config module:

```python
import pandas as pd
from dev.src import config

def read_sql_file(query_path, connection, **params):
    """Load data from a SQL database using a parameterised SQL file."""
    with open(query_path, 'r') as f:
        sql = f.read().format(**params)
    return pd.read_sql(sql, connection)
```

The key principle is provider-agnostic: keep SQL separate from Python, parameterise through function arguments and small config constants, and centralise I/O in `dev/src/io.py`. Swap `pd.read_sql` for `pd.read_gbq`, `snowflake.connector`, or any other client as needed.

## Column Standardisation Helpers

When working with messy source data, standardise column names immediately:

```python
def name_lock(df):
    """Generate a name-mapping dict: original → snake_case."""
    names = df.columns
    std = names.map(lambda x: x.replace("-", "_").replace(" ", "_").lower())
    return dict(zip(names, std))

def type_lock(df):
    """Generate a type-mapping dict: column → dtype string."""
    return {col: str(df[col].dtype) for col in df.columns}
```

## AGENTS.md — How to Write One for Analytics Projects

Every analytics project should include an `AGENTS.md` file in its root. This file tells AI coding agents **how to work with this specific project**. Here's the template:

```markdown
# AGENTS.md

## Project Overview

[One-paragraph description: what this project does, what business question it answers.]

## Tech Stack

- **Python** [version] with [venv/uv]
- **Data platform:** [database / data warehouse / local files]
- **Storage:** [cloud storage / local filesystem]
- **Key libraries:** [pandas, scikit-learn, xgboost, etc.]

## Project Structure

[Copy the folder tree from this skill, adapted to the project's specifics.]

## Working with This Project

### Setup
1. Clone the repository
2. Create virtual environment: `python -m venv .venv` (or `uv sync`)
3. Install dependencies: `pip install -r requirements.txt`
4. Set up pre-commit hook for notebook output clearing
5. Copy `.env.example` → `.env` and fill in credentials

### Running Notebooks
- Notebooks are numbered and must be run in order: `01_`, `02_`, …
- Each notebook imports shared config/constants from `dev/src/` as needed
- `dev/` notebooks are for experimentation; `prod/` notebooks are production-ready

### Data
- Raw data is loaded from [database / cloud storage] via SQL scripts in `dev/sql/`
- Never commit data files — they are in `.gitignore`
- Processed data goes to `data/processed/`

### Models
- Trained models are saved as `.pkl` files in `dev/models/` or `prod/models/`
- Always version model artifacts with a descriptive name

### Branching & Commits
- Branch prefixes: `data/`, `analysis/`, `model/`, `bugfix/`, `release/`
- Commit messages: English, imperative, capitalised, 3–7 words, no punctuation

## Code Conventions

- Import shared config/constants at the top of every notebook
- Use `dev/src/` modules for reusable logic — don't duplicate code across notebooks
- Use `%load_ext autoreload` and `%autoreload 2` for hot-reloading during development
- Set `warnings.filterwarnings('ignore')` only in production notebooks
- Clear notebook outputs before committing (pre-commit hook handles this)

## Key Decisions & Context

[Document important choices: why this model type, why this feature set, known data quality issues, stakeholder constraints.]

## Related Skills

When working on this project, the agent should also reference:
- `ml-modeling` — for model building patterns
- `statistical-modeling` — for inferential analysis
- `data-warehousing` — for data pipeline patterns
- `designing-analytics-projects` — for the project brief
```

### AGENTS.md Best Practices

1. **Be specific to the project.** Generic advice belongs in skills, not AGENTS.md.
2. **Document the data lineage.** Where does the data come from? What SQL/queries generate it?
3. **List known gotchas.** "Column X has 30% missing values", "Table Y is refreshed weekly on Mondays".
4. **Document your config source.** Show where paths, table names, and constants are defined.
5. **Keep it updated.** AGENTS.md rots faster than code — review it when you change the project structure.

## README.md Template for Analytics Projects

Keep READMEs structured consistently (aligned with Géron's "Frame the problem" checklist):

```markdown
# [Project Name]

[One-sentence description.]

## 1. Objective
[Business goal. How will the solution be used?]

## 2. Project Structure
[Folder tree, key notebooks, data sources.]

## 3. Setup
[Clone, install deps, configure .env and shared config constants.]

## 4. References
[Decision sources, related projects, documentation links.]
```

## Anti-Patterns to Flag

- **No `dev/prod` separation.** Everything in one folder → messy handoff to production.
- **Unnumbered notebooks.** No one knows what order to run them.
- **Scattered hardcoded paths** instead of shared config/constants.
- **Committed `.env` files** with secrets.
- **Committed data files** or notebook outputs.
- **No `__init__.py` in `src/`.** Imports fail.
- **Copy-pasted utility functions** across notebooks instead of using `dev/src/`.
- **No pre-commit hook.** Notebook outputs leak into version control.
- **Using `master` directly** instead of feature branches.
- **No README or AGENTS.md.** New team members (and AI agents) are lost.
- **Unpinned production dependencies.** `pip install pandas` today ≠ `pip install pandas` next month.
- **`pyvenv.cfg` committed.** It's machine-specific. Add to `.gitignore`.

## Initialising a New Project (Step-by-Step)

When asked to set up a new analytics project:

1. **Create the repository** following the folder structure above.
2. **Update `README.md`** with project-specific info (business requirements, scope, links).
3. **Create `AGENTS.md`** using the template above.
4. **Create shared config/constants** in `dev/src/config.py` for paths and table names.
5. **Set up virtual environment** (`uv init` or `python -m venv .venv`).
6. **Install pre-commit hook** for notebook output clearing.
7. **Set `git config core.ignoreCase false`.**
8. **Remove `data/` and `dev/visualization/` from git cache** if inherited from template.
9. **Create initial notebooks** with numbered prefixes: `01_data_collection.ipynb`, `02_eda.ipynb`, etc.
10. **Create `.env.example`** with placeholder keys (no real values).
11. **Commit** with message: `Initialise analytics project structure`.

## Further Reference

- Use this skill's folder structure and conventions as your starting point.
- Géron, [*Hands-On Machine Learning*](https://github.com/ageron/handson-ml3) — ch. 2 (end-to-end project) is the canonical walkthrough of the workflow this structure supports.
- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) — the open-source inspiration for this folder structure.
- [DVC](https://dvc.org/) — if the team needs data versioning beyond `.gitignore`.
- `ml-modeling` skill — for model building patterns and the `ResultCollector` leaderboard.
- `statistical-modeling` skill — for inferential analysis patterns.
- `data-warehousing` skill — for bronze/silver/gold data pipeline patterns.
- `designing-analytics-projects` skill — for the pre-code Analytics Project Brief.
- `uv` skill — for modern Python environment management.

---

*The single highest-leverage habit: **start with a clean structure, not ad-hoc files.** The structure is the value.*

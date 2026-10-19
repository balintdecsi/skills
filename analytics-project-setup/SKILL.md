---
name: analytics-project-setup
description: Technical setup skill for analytics and data science projects — repository scaffolding, mandatory dev/prod and bronze/silver/gold structure, numbered notebooks, uv environments, dotenv, notebook-output hooks, branching and Conventional Commits, .gitignore patterns, README and AGENTS.md creation, database/storage I/O patterns, and production orchestration notebooks. Use when initialising or restructuring an analytics repository, setting up its environment or documentation, configuring team Git conventions, or deploying notebook workflows to production.
---

# Analytics Project Setup — Technical Guide

These are **codified best practices** for scaffolding, configuring, and maintaining analytics and data science project repositories. The patterns are distilled from production analytics experience and industry-standard practices from [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) and Géron's [*Hands-On Machine Learning*](https://github.com/ageron/handson-ml3).

They adapt to any cloud (GCP, AWS, Azure) or local stack.

## The Canonical Folder Structure

Every project follows this layout. The `dev/` and `prod/` split is the single most important structural decision — it separates exploratory work from production-grade code.

```
├── data/                                    # Data (ignored unless explicitly tracked)
│   ├── external/                            # Third-party / lookup data
│   ├── bronze/                              # Immutable source snapshots
│   ├── silver/                              # Cleaned, typed, validated data
│   ├── gold/                                # Business-ready datasets
│   │   ├── train_sample.csv
│   │   └── test_sample.csv
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
│   │   └── datadrift_psi.py                 # Data drift monitoring (PSI)
│   └── visualization/                       # Generated plots, figures
│
├── examples/                                # Reference notebooks & templates
│   ├── EDA_notebook.ipynb
│   ├── datadrift_psi_example.ipynb
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
├── pyproject.toml                            # Project metadata and dependencies
├── uv.lock                                   # Reproducible dependency lock
├── AGENTS.md                                # AI agent instructions (see below)
└── README.md                                # Project documentation
```

### Key Structural Rules

1. **Number notebooks by execution order:** `01_`, `02_`, `03_`, … This makes the workflow self-documenting.
2. **`dev/` is your sandbox, `prod/` is sacred.** Experimental code stays in `dev/`. Only reviewed, stable code moves to `prod/`.
3. **Ignore `data/` by default.** Track only small samples or intentional artifacts when the project explicitly documents that choice.
4. **Ignore `dev/visualization/` by default.** Track a generated figure only when it is an intentional project artifact.
5. **`dev/src/` contains reusable modules** — import these in notebooks, don't copy-paste code between cells.
6. **`examples/` contains reference material** — EDA templates, environment setup examples, data drift examples.
7. **Keep runtime config minimal.** Start with environment variables and small Python config modules; add heavier config layers only when needed.

## Lightweight Configuration Pattern

Skip heavyweight config files at first. Use `.env` for secrets and a tiny Python module for paths and table names:

```python
# dev/src/config.py
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
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

Use Conventional Commits with short, imperative summaries:

Examples:

- `feat(data): add feature engineering notebook`
- `fix(pipeline): prevent duplicate table rows`
- `chore: ignore generated documentation`
- `refactor(model): compare tree-based candidates`

## Environment Management

Use `uv` for new projects (see the `uv` skill for details). Confirm the
dependency set with the user before adding or installing packages:

```bash
uv init
uv add pandas scikit-learn matplotlib numpy scipy
uv add --dev ipykernel jupyter nbconvert
```

### Existing legacy projects

Preserve an existing `venv` + `requirements.txt` workflow rather than migrating it implicitly:

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
joblib
```

Pin versions for production (`matplotlib==3.7.2`). Leave unpinned in dev for flexibility.

### Environment Variables with `dotenv`

For secrets (API keys, database credentials) that must **never** be committed:

```bash
uv add python-dotenv
```

Create `.env` in project root (already in `.gitignore`):

```
DB_PASSWORD=
API_KEY=
```

Load in notebooks:

```python
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("DB_PASSWORD")
```

## Pre-commit Hook: Clearing Notebook Outputs

As required by `AGENTS.md`, clear every notebook output before committing. Document this local Git hook at `.git/hooks/pre-commit` and install it after each clone:

```bash
cat > .git/hooks/pre-commit <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

# Clear outputs for staged notebooks only, then re-stage them.
staged_notebooks="$(git diff --cached --name-only --diff-filter=ACM -- '*.ipynb')"
[ -z "${staged_notebooks}" ] && exit 0

if [ -f uv.lock ]; then
  command -v uv >/dev/null || {
    echo "uv is required to clear notebook outputs in this project" >&2
    exit 1
  }
  nbconvert=(uv run jupyter nbconvert)
else
  nbconvert=(jupyter nbconvert)
fi

while IFS= read -r notebook; do
  [ -f "${notebook}" ] || continue
  "${nbconvert[@]}" --ClearOutputPreprocessor.enabled=True --inplace "${notebook}"
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
from dev.src.config import ROOT

notebook_dir = ROOT / "prod" / "notebooks"
notebooks = [
    "01_precheck.ipynb",
    "02_features.ipynb",
    "03_modelling.ipynb",
    "04_evaluation.ipynb",
]

for notebook in notebooks:
    file = notebook_dir / notebook
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

Centralise data access through SQL files, bound value parameters, and a small config module:

```python
import pandas as pd
from dev.src import config

def read_sql_file(query_path, connection, params=None):
    """Load data using the database driver's bound-value parameters."""
    with open(query_path, 'r') as f:
        sql = f.read()
    return pd.read_sql(sql, connection, params=params)

# With a SQLAlchemy connection, orders.sql can contain:
# SELECT * FROM orders WHERE customer_id = :customer_id
orders = read_sql_file("dev/sql/orders.sql", connection, {"customer_id": 42})
```

Keep SQL separate from Python and centralise I/O in `dev/src/io.py`. Bind untrusted values through the database API; use carefully validated templating only for identifiers that the driver cannot bind. Swap `pd.read_sql` for `pd.read_gbq`, `snowflake.connector`, or another client as needed.
Placeholder syntax is driver-specific (`:name`, `?`, or `%s`), so match the
connection library rather than interpolating values into the SQL string.

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

Every analytics project should receive the user's generic `AGENTS.md` as its
base policy. Preserve that policy and append only project-specific context; do
not fork generic Git, dependency, review, notebook-output, or safety rules into
a second template.

```markdown
## Project Overview

[One-paragraph description: what this project does, what business question it answers.]

## Tech Stack

- **Python** [version] with [venv/uv]
- **Data platform:** [database / data warehouse / local files]
- **Storage:** [cloud storage / local filesystem]
- **Key libraries:** [pandas, scikit-learn, xgboost, etc.]

## Project Structure

[Copy the folder tree from this skill, adapted to the project's specifics.]

## Project Workflow

- Notebooks are numbered and must be run in order: `01_`, `02_`, …
- Each notebook imports shared config/constants from `dev/src/` as needed
- `dev/` notebooks are for experimentation; `prod/` notebooks are production-ready

### Data
- Raw data is loaded from [database / cloud storage] via SQL scripts in `dev/sql/`
- Data is ignored by default; list any intentionally tracked samples or artifacts
- Raw snapshots go to `data/bronze/`, cleaned data to `data/silver/`, and business-ready data to `data/gold/`

### Models
- Trained models are saved as `.pkl` files in `dev/models/` or `prod/models/`
- Always version model artifacts with a descriptive name

## Key Decisions & Context

[Document important choices: why this model type, why this feature set, known data quality issues, stakeholder constraints.]

## Related Skills

[List only the domain skills relevant to this project.]
```

### AGENTS.md Best Practices

1. **Keep the generic base policy intact.** Add project facts rather than rewriting shared rules.
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
- **Undocumented committed data files or generated artifacts**, or any committed notebook outputs.
- **No `__init__.py` in `src/`.** Imports fail.
- **Copy-pasted utility functions** across notebooks instead of using `dev/src/`.
- **No pre-commit hook.** Notebook outputs leak into version control.
- **Using `master` directly** instead of feature branches.
- **No README or AGENTS.md.** New team members (and AI agents) are lost.
- **Unpinned production dependencies.** `pip install pandas` today ≠ `pip install pandas` next month.
- **`pyvenv.cfg` committed.** It's machine-specific. Add to `.gitignore`.

## Initialising a New Project (Step-by-Step)

When asked to set up a new analytics project:

1. **Create a topic branch** and scaffold the repository using the folder structure above.
2. **Update `README.md`** with project-specific info (business requirements, scope, links).
3. **Copy the generic `AGENTS.md` policy** and append the project-specific context above.
4. **Create shared config/constants** in `dev/src/config.py` for paths and table names.
5. **After the user approves the dependency set, set up the uv project and environment** (`uv init`; add the project dependencies and `ipykernel`, `jupyter`, and `nbconvert`; then `uv sync`).
6. **Install the documented local pre-commit hook** for notebook output clearing.
7. **Set `git config core.ignoreCase false`.**
8. **Remove `data/` and `dev/visualization/` from git cache** if inherited from template.
9. **Create initial notebooks** with numbered prefixes: `01_data_collection.ipynb`, `02_eda.ipynb`, etc.
10. **Create `.env.example`** with placeholder keys (no real values).
11. **Commit** with message: `chore: initialize analytics project structure`.

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
- `legal-compliance` skill — for `LICENSE` / `THIRD-PARTY-NOTICES.md` at scaffold time, and for
  GDPR obligations when the project stores data about identifiable people.

---

*The single highest-leverage habit: **start with a clean structure, not ad-hoc files.** The structure is the value.*

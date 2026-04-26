---
name: data-warehousing
description: Best practices for designing data warehouses and analytical pipelines using the bronze/silver/gold medallion architecture, validations-as-code, and idempotent transforms. Use when building or modifying data pipelines, ETL/ELT jobs, dbt models, SQL warehouses, lakehouses, or any layered analytics workload (DuckDB, Snowflake, BigQuery, Postgres, Spark, etc.).
---

# Data Warehousing Best Practices

These best practices are based on my (the user's) university masters course **ECBS5294 — Introduction to Data Science: Working with Data** at Central European University, taught by Eduardo Ariño de la Rubia. The user particularly liked the **bronze → silver → gold** layered division and the **validations-as-code** discipline, and wants those principles applied consistently.

The guidance is **tool-agnostic**. The user is not always using DuckDB — apply the same patterns whether the warehouse is DuckDB, Snowflake, BigQuery, Redshift, Postgres, Databricks/Spark, ClickHouse, or a dbt project on top of any of them.

**Upstream source for further reference:** <https://github.com/earino/ECBS5294> (course repository the user inspired this skill from — check it for full notebooks, slides and worked examples).

## When to Use

Apply this skill whenever the user is:

- Designing or modifying a data warehouse / lakehouse / analytics database.
- Writing or reviewing ETL/ELT pipelines, dbt models, Airflow DAGs, notebooks, or SQL transforms.
- Adding tests, assertions, or data-quality checks.
- Modeling tables (fact/dimension, normalization, primary keys).
- Ingesting CSV / JSON / API / Parquet sources into analytical tables.
- Reviewing somebody else's pipeline code.

## Core Principles (the non-negotiables)

1. **Layer your pipeline: bronze → silver → gold.** Never collapse all transforms into one step.
2. **Validations are code, not vibes.** Every layer has explicit assertions that fail loudly.
3. **Idempotent transforms.** Re-running a step must produce the same result — use `CREATE OR REPLACE`, `MERGE`, or `if_exists='replace'`, never blind appends.
4. **Fail fast.** Detect bad data at the boundary it arrives. Do not let `NaN`/`NaT`/`NULL` silently propagate.
5. **Bronze is read-only.** The raw landing zone is an audit trail; never edit it in place.
6. **Document assumptions next to the code** that depends on them (a comment on the filter, not a wiki page).
7. **Reproducibility:** relative paths, pinned dependencies, "Run-All from a clean clone" must succeed.

## The Medallion Architecture (bronze / silver / gold)

```
SOURCE → [BRONZE] → [SILVER] → [GOLD] → CONSUMERS
         raw,       cleaned,    business
         immutable  validated,  metrics,
                    typed       aggregated,
                                joined
```

### Bronze — preserve the raw

- Land data **exactly as received**. No casts, no filtering, no renames.
- One bronze table per source (`bronze_orders`, `bronze_nyc_permits_json`, ...).
- Capture lineage columns when cheap: `_ingested_at`, `_source_file`, `_source_row_number`.
- Treat bronze as an **append-only or replace-only archive**. If reprocessing, drop & reload from source — never mutate.

### Silver — clean, typed, validated

This is the analyst-friendly foundation. Every silver table must be:

- **Correctly typed** (`DATE`, `DECIMAL`, `BOOLEAN`, not strings everywhere).
- **PK-validated** (unique, non-null).
- **Standardized** (trimmed whitespace, normalized casing for join keys, canonical NULL representation).
- **Filtered of structurally-invalid rows**, with the filter reason documented.
- **Covered by assertions** that run as part of the build.

### Gold — business-specific marts

- Joined, denormalized, aggregated to answer specific business questions.
- Multiple gold tables are encouraged: one per business domain (`gold_daily_revenue`, `gold_customer_ltv`, `gold_product_performance`).
- Optimized for **read performance and clarity**, not for storage.
- Stable column names — these are the contract with downstream consumers (BI tools, ML features, stakeholders).

For deeper guidance on each layer (responsibilities, anti-patterns, naming), see [reference/layers.md](reference/layers.md).

## Validations as Code

Every silver and gold table needs explicit checks. Minimum bar:

| Check | Why |
|---|---|
| **PK uniqueness** | Without it, joins inflate silently. |
| **PK non-null** | NULL keys break referential integrity. |
| **Required-fields non-null** | Catches upstream schema drift. |
| **Value-range / domain checks** | Negative prices, future birthdates, unknown enum values. |
| **Row-count sanity** | Compare to expected magnitude or to previous run (±X%). |
| **Referential integrity (FK)** | Every `customer_id` in `orders` exists in `customers`. |

Run validations **inside the pipeline**, not in a separate "QA notebook". A failure must stop the build, not just print a warning.

For a copy-pasteable catalogue of checks in SQL and Python, see [reference/validations.md](reference/validations.md) and the snippets under [snippets/](snippets/).

## Idempotency

A pipeline step is **idempotent** if running it N times produces the same result as running it once.

Patterns that are idempotent:

- `CREATE OR REPLACE TABLE silver_x AS SELECT ...`
- `DROP TABLE IF EXISTS silver_x; CREATE TABLE silver_x AS ...`
- `MERGE INTO target USING source ON ... WHEN MATCHED ... WHEN NOT MATCHED ...`
- `df.to_sql(..., if_exists='replace')` or writing to a partition with overwrite semantics.

Patterns that are **not** idempotent (avoid unless you really mean it):

- `INSERT INTO ... SELECT ...` without a dedup/merge step.
- `df.to_sql(..., if_exists='append')` in a notebook that may be re-run.
- Mutating bronze in place.

## Modeling Cheatsheet

- **Tidy data first** (Wickham): one variable per column, one observation per row, one observational unit per table.
- Identify the **grain** of every table in one sentence ("one row per order line per day"). If you can't, the model is wrong.
- Prefer **surrogate keys** (`order_sk BIGINT`) for joins; keep natural keys as attributes for traceability.
- Use **composite keys** when the grain is naturally multi-column (`store_id, date`).
- For analytics, **star schemas** (fact + dimensions) age well; full 3NF is rarely worth it in a warehouse.

## SQL Style (warehouse-flavor)

- Uppercase keywords, lowercase identifiers, one clause per line, trailing commas off.
- Always alias tables in joins (`o`, `c`) and qualify every column.
- Prefer `LEFT JOIN` + explicit `WHERE right_table.id IS NULL` for anti-joins (clearer than `NOT IN`, NULL-safe).
- Use CTEs (`WITH`) to layer logic; avoid deep nested subqueries.
- Use `TRY_CAST` (or the engine's safe-cast equivalent) on untrusted source data; bare `CAST` belongs only on already-validated silver.
- Handle NULLs explicitly with `IS NULL`, `IS NOT NULL`, `COALESCE`. Never compare with `= NULL`.

## Recommended Workflow

When asked to build or modify a pipeline:

1. **Identify the grain** of each target table. State it explicitly.
2. **Sketch the layers**: which sources land in bronze, what cleaning happens in silver, which marts in gold.
3. **Define the PK** and the validations for every silver/gold table *before* writing the SELECT.
4. **Write the transform** with `CREATE OR REPLACE` / `MERGE` (idempotent).
5. **Add assertions** immediately after the transform — in the same script/model.
6. **Run end-to-end on a small sample**, then on full data.
7. **Document assumptions** as inline comments where they bite (e.g. "NULL price = quote pending, excluded from revenue").

## Code Snippets (tool-agnostic)

Ready-to-adapt examples live in [snippets/](snippets/):

- `snippets/bronze_silver_gold.sql` — full layered pipeline in plain ANSI-ish SQL with `CREATE OR REPLACE`.
- `snippets/validations.sql` — PK uniqueness, non-null, FK, range, row-count checks as SELECTs that should return zero rows.
- `snippets/validations.py` — the same checks as Python `assert` statements (works against any DB-API connection or a pandas DataFrame).
- `snippets/dbt_tests.yml` — equivalent expressed as dbt schema tests for projects using dbt.

Pick the flavor that matches the user's stack; the *patterns* are the same.

## Anti-Patterns (call these out in reviews)

- **One giant notebook** doing load + clean + analyze with no layer separation.
- **Silent coercion** (`errors='coerce'`, default-NULL casts) without a follow-up assertion.
- **Appending without a key** — the classic "double-the-data on re-run" bug.
- **No PK declared / no PK test** on a fact table.
- **Cleaning in bronze** ("we'll just trim the strings on load") — destroys the audit trail.
- **One mega "gold" table** trying to answer every question — split by business domain.
- **Validations in a separate notebook** that nobody runs.
- **Absolute paths** (`/Users/me/...`) breaking reproducibility.
- **Magic numbers** in filters with no comment explaining the business reason.

## Data Sources Used in the Course (good for practice pipelines)

`ECBS5294` deliberately uses small, deliberately *messy* datasets so the bronze→silver→gold
journey actually has work to do at every layer. They are excellent for prototyping a new pipeline
or testing validation snippets:

| Dataset | What's messy about it | URL |
|---|---|---|
| Cafe Sales — Dirty Data for Cleaning Training | NULLs as `"ERROR"` / `"UNKNOWN"`, mixed types, broken dates, ~10k rows | <https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training> |
| Retail Store Sales — Dirty for Data Cleaning | Inconsistent categories, missing values, ~12.5k rows | <https://www.kaggle.com/datasets/ahmedmohamed2003/retail-store-sales-dirty-for-data-cleaning> |

Other good free sources for end-to-end warehouse practice:

| Source | Why useful | URL |
|---|---|---|
| NYC TLC trip data (Yellow / Green / FHV) | Big, partitioned by month, schema drifts over years — perfect bronze→silver work | <https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page> |
| TPC-H sample (any size) | Canonical multi-table star-schema dataset for gold-layer modeling exercises | <https://www.tpc.org/tpch/> |
| Kaggle "datasets" tag `data-cleaning` | Curated dirty datasets for ETL practice | <https://www.kaggle.com/datasets?tags=14201-Data+Cleaning> |
| OpenFlights | Multi-table joins (airports, airlines, routes) — great Silver-layer dimensional modeling | <https://openflights.org/data.html> |
| World Bank Open Data | Wide → long reshape, plus codebook joins for Silver | <https://data.worldbank.org/> |
| dbt-labs `jaffle_shop` | Tiny demo ecommerce dataset used in dbt tutorials | <https://github.com/dbt-labs/jaffle_shop> |

For new projects, default to: **CSV/Parquet into Bronze**, **Parquet into Silver/Gold**.
Document source URL, download date, and licence next to the load.

## Further Reference

- **Upstream course repo (the inspiration):** <https://github.com/earino/ECBS5294>
  - `references/pipeline_patterns_quick_reference.md` — original bronze/silver/gold quick reference.
  - `references/tidy_data_checklist.md` — tidy data + PK validation patterns.
  - `notebooks/day3/day3_block_a_pipelines_and_validations.ipynb` — full worked example.

Production analytics project templates (database I/O patterns):

- Reusable analytics project patterns — include `dev/src/io.py` style SQL helpers, EDA utilities, and shared config/constants modules.

Companion skills:

- **`analytics-project-setup`** — folder structure, database/storage I/O helpers, AGENTS.md, environment management.
- **`ml-modeling`** — for the modelling phase that consumes the gold-layer data.
- **`statistical-modeling`** — for inferential analysis on cleaned data.
- **`designing-analytics-projects`** — for the pre-code project brief.

External:

- Hadley Wickham, *Tidy Data* (2014).
- Kimball & Ross, *The Data Warehouse Toolkit* — for star-schema and dimensional modeling depth.
- dbt docs on tests and model contracts: <https://docs.getdbt.com/docs/build/data-tests>.
- Databricks "Medallion architecture" overview (the bronze/silver/gold naming convention).

---

*This skill encodes the user's preferred pipeline discipline. When in doubt, prefer **more layers and more assertions** over cleverness in a single step.*

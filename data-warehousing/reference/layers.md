# Bronze / Silver / Gold — Layer Responsibilities

Detailed guidance for each medallion layer. Source-inspired by the ECBS5294 course materials at <https://github.com/earino/ECBS5294>.

---

## Bronze — the raw landing zone

**Purpose:** preserve source data **exactly as received** so we can always reprocess from a known-good starting point.

### Allowed
- Reading from source (file, API, queue, replication stream).
- Adding **lineage columns**: `_ingested_at`, `_source_file`, `_source_row_number`, `_source_system`.
- Light structural framing for semi-structured input (e.g. one row per JSON document, the document kept as `JSON`/`VARIANT`/`JSONB`).

### Forbidden
- Type casting (other than parsing the container).
- Filtering, deduping, renaming.
- Joining, enriching, aggregating.
- Mutating in place. **Bronze is replace-or-append, never update.**

### Naming
- Prefix `bronze_` (or schema `bronze.`).
- Keep the source name visible: `bronze_orders_csv`, `bronze_nyc_permits_json`.

### Storage
- Columnar (Parquet/Iceberg/Delta) when volume is meaningful.
- Partition by ingestion date when reprocessing windows matter.

---

## Silver — clean, typed, validated

**Purpose:** the analyst-friendly truth. Anything downstream can trust silver.

### Required transforms
1. **Cast to correct types** (`DATE`, `TIMESTAMP`, `DECIMAL(p,s)`, `BOOLEAN`, etc.).
2. **Standardize**: trim whitespace, lowercase join keys (emails, codes), canonical NULL.
3. **Deduplicate** to the declared grain (often via `ROW_NUMBER() OVER (PARTITION BY pk ORDER BY _ingested_at DESC) = 1`).
4. **Filter structurally invalid rows** (NULL PK, impossible dates) — *with a comment explaining the rule*.
5. **Validate** with assertions (PK uniqueness, non-null, FK, ranges).

### Forbidden
- Business-specific aggregation (that's gold's job).
- Hardcoded report filters ("only North America customers") — keep silver business-neutral.
- Mixing multiple grains in one table.

### Naming
- Prefix `silver_` (or schema `silver.`).
- Name reflects the entity, not the source: `silver_orders`, `silver_customers`, `silver_order_items`.

### One silver table per entity at one grain
If you need orders at order-grain and at line-grain, that's two silver tables (`silver_orders`, `silver_order_lines`).

---

## Gold — business-specific marts

**Purpose:** answer specific business questions fast and clearly.

### Allowed and encouraged
- Joins across silver tables.
- Aggregations to reporting grain (daily, monthly, per-customer).
- Denormalization for read performance.
- Hardcoded business filters and definitions ("active customer = order in last 90 days") — *with a comment*.
- Multiple gold tables, one per business question / domain.

### Required
- Stable, documented column names (this is the contract with BI / ML / stakeholders).
- Validations on aggregate sanity (totals match silver, no unexpected NULLs).

### Naming
- Prefix `gold_` and describe the *question*: `gold_daily_revenue_by_category`, `gold_customer_ltv`, `gold_active_users_weekly`.

### Anti-pattern: the "one big gold table"
Resist building a 200-column wide table that "has everything". Split by domain — each gold table should be understandable in one paragraph.

---

## When to add layers beyond bronze/silver/gold

Sometimes useful, often premature:

- **Staging / `stg_`** (dbt convention): a thin renaming/casting layer between bronze and silver. Worth it when source column names are awful or you have many sources to harmonize.
- **Platinum / semantic layer**: BI-tool-specific cubes or metric definitions. Only when a BI tool demands it.

Default to three layers. Add more only when you can name the concrete pain it solves.

---

## Quick checklist before declaring a pipeline "done"

- [ ] Each table has its **grain** documented in one sentence.
- [ ] Each silver/gold table has a **declared PK** and a **uniqueness assertion**.
- [ ] Required fields have **non-null assertions**.
- [ ] Every transform uses `CREATE OR REPLACE` / `MERGE` (idempotent).
- [ ] Bronze is untouched after ingest.
- [ ] No absolute paths.
- [ ] Re-running end-to-end produces identical output.
- [ ] Assumptions baked into filters are commented inline.

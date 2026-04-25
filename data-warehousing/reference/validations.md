# Validations as Code — Catalogue

Source-inspired by the ECBS5294 course materials at <https://github.com/earino/ECBS5294>.

The contract: **every check returns zero rows (SQL) or evaluates to `True` (Python). Anything else fails the build.**

---

## The minimum bar (don't ship without these)

1. **Primary key uniqueness**
2. **Primary key non-null**
3. **Required-fields non-null**
4. **Domain / range** on critical numeric and enum columns
5. **Referential integrity** for every declared FK
6. **Row-count sanity** (within expected range, or within ±X% of last run)

Add business-rule checks on top, but never below this bar.

---

## SQL pattern: assertions as zero-row queries

A check is a `SELECT` that should return **no rows**. Wrap them in your orchestrator (Airflow, dbt test, plain script) and fail when row count > 0.

```sql
-- 1. PK uniqueness
SELECT order_id, COUNT(*) AS n
FROM silver_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 2. PK non-null
SELECT 1 FROM silver_orders WHERE order_id IS NULL;

-- 3. Required field non-null
SELECT 1 FROM silver_orders WHERE customer_id IS NULL;

-- 4. Range / domain
SELECT 1 FROM silver_order_items WHERE price < 0 OR quantity <= 0;
SELECT 1 FROM silver_orders WHERE status NOT IN ('pending', 'completed', 'cancelled');

-- 5. Referential integrity (FK)
SELECT o.customer_id
FROM silver_orders o
LEFT JOIN silver_customers c USING (customer_id)
WHERE c.customer_id IS NULL;

-- 6. Date sanity
SELECT 1 FROM silver_orders
WHERE order_date < DATE '2015-01-01' OR order_date > CURRENT_DATE;
```

---

## Python pattern: `assert` next to the transform

```python
n_rows = con.execute("SELECT COUNT(*) FROM silver_orders").fetchone()[0]
n_unique = con.execute("SELECT COUNT(DISTINCT order_id) FROM silver_orders").fetchone()[0]
assert n_rows == n_unique, f"PK not unique: {n_rows=} {n_unique=}"

n_null_pk = con.execute("SELECT COUNT(*) FROM silver_orders WHERE order_id IS NULL").fetchone()[0]
assert n_null_pk == 0, f"NULL PK rows: {n_null_pk}"

n_orphans = con.execute("""
    SELECT COUNT(*) FROM silver_orders o
    LEFT JOIN silver_customers c USING (customer_id)
    WHERE c.customer_id IS NULL
""").fetchone()[0]
assert n_orphans == 0, f"Orphan customer_id in orders: {n_orphans}"
```

For pandas DataFrames the equivalents are:

```python
assert df['order_id'].is_unique, "Duplicate order_id"
assert df['order_id'].notna().all(), "NULL order_id"
assert (df['price'] >= 0).all(), "Negative price"
assert df['customer_id'].isin(customers['customer_id']).all(), "Orphan customer_id"
```

---

## dbt-flavored equivalents

If the user's project is dbt, prefer the schema-test format:

```yaml
version: 2
models:
  - name: silver_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('silver_customers')
              field: customer_id
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'completed', 'cancelled']
```

For business-rule checks beyond the built-ins, write a singular test in `tests/` or use `dbt-utils` / `dbt-expectations`.

---

## Row-count drift detection

Catches "the upstream API returned an empty page and we silently produced an empty mart":

```sql
-- Compare current run to a stored baseline (e.g. previous day's row count)
WITH current_count AS (SELECT COUNT(*) AS n FROM gold_daily_revenue),
     baseline    AS (SELECT n AS n_prev FROM ops_row_count_log
                      WHERE table_name = 'gold_daily_revenue'
                      ORDER BY run_at DESC LIMIT 1)
SELECT 1
FROM current_count, baseline
WHERE n < n_prev * 0.5    -- dropped by >50%
   OR n > n_prev * 2.0;   -- doubled (re-ingest bug?)
```

---

## What a "good" failure message looks like

Bad: `AssertionError`

Good: `AssertionError: silver_orders PK not unique: 12 duplicates among 1,204,553 rows. Sample dup keys: [..., ..., ...]`

Always include: which check, which table, the magnitude, and a sample. The person debugging at 3am will thank you.

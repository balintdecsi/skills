-- =============================================================================
-- Bronze / Silver / Gold pipeline — tool-agnostic SQL template
-- Inspired by ECBS5294 course materials: https://github.com/earino/ECBS5294
--
-- Adapt to your engine:
--   * DuckDB / Postgres / Snowflake / BigQuery / Redshift / ClickHouse all
--     support CREATE OR REPLACE TABLE (or CREATE OR REPLACE VIEW). On engines
--     that don't, use DROP TABLE IF EXISTS + CREATE TABLE.
--   * TRY_CAST exists in DuckDB / Snowflake / BigQuery (as SAFE_CAST).
--     For Postgres, wrap with a function or use a CASE+regex guard.
-- =============================================================================


-- -----------------------------------------------------------------------------
-- BRONZE — raw, no transformations, lineage columns only
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE bronze_orders AS
SELECT
    *,
    CURRENT_TIMESTAMP        AS _ingested_at,
    'orders_2025_10_22.csv'  AS _source_file
FROM read_csv_auto('data/raw/orders_2025_10_22.csv');   -- engine-specific source read


-- -----------------------------------------------------------------------------
-- SILVER — typed, deduped, validated, business-neutral
-- Grain: one row per order_id
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE silver_orders AS
WITH typed AS (
    SELECT
        TRY_CAST(order_id     AS BIGINT)         AS order_id,
        TRY_CAST(customer_id  AS BIGINT)         AS customer_id,
        TRY_CAST(order_date   AS DATE)           AS order_date,
        TRY_CAST(total_amount AS DECIMAL(12,2))  AS total_amount,
        LOWER(TRIM(status))                      AS status,
        _ingested_at,
        _source_file
    FROM bronze_orders
),
-- Dedup to declared grain: keep the most recently ingested row per PK.
deduped AS (
    SELECT *
    FROM (
        SELECT
            t.*,
            ROW_NUMBER() OVER (
                PARTITION BY order_id
                ORDER BY _ingested_at DESC
            ) AS _rn
        FROM typed t
        WHERE order_id IS NOT NULL              -- structural: drop NULL PKs
    ) ranked
    WHERE _rn = 1
)
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    status,
    _ingested_at,
    _source_file
FROM deduped
WHERE order_date IS NOT NULL                    -- ASSUMPTION: rows missing a date are unusable
  AND total_amount >= 0                         -- ASSUMPTION: refunds arrive on a separate feed
  AND status IN ('pending', 'completed', 'cancelled');


-- -----------------------------------------------------------------------------
-- GOLD — business-specific mart
-- Question: "What is daily revenue by status?"
-- Grain: one row per (order_date, status)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE gold_daily_revenue_by_status AS
SELECT
    order_date                            AS date,
    status,
    COUNT(*)                              AS n_orders,
    SUM(total_amount)                     AS revenue,
    AVG(total_amount)                     AS avg_order_value
FROM silver_orders
GROUP BY order_date, status
ORDER BY date, status;

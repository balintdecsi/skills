-- =============================================================================
-- Validations as code — every query below MUST return zero rows.
-- Wire these into your orchestrator (Airflow sensor, dbt test, plain script):
-- if any returns > 0 rows, fail the build.
--
-- Inspired by ECBS5294: https://github.com/earino/ECBS5294
-- =============================================================================


-- -- silver_orders --------------------------------------------------------------

-- 1. PK uniqueness
SELECT order_id, COUNT(*) AS n
FROM silver_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 2. PK non-null
SELECT 'silver_orders.order_id is NULL' AS failure
FROM silver_orders
WHERE order_id IS NULL;

-- 3. Required field non-null
SELECT 'silver_orders.customer_id is NULL' AS failure
FROM silver_orders
WHERE customer_id IS NULL;

-- 4. Domain check
SELECT 'silver_orders.status not in allowed set' AS failure, status
FROM silver_orders
WHERE status NOT IN ('pending', 'completed', 'cancelled');

-- 5. Range check
SELECT 'silver_orders.total_amount negative' AS failure, order_id, total_amount
FROM silver_orders
WHERE total_amount < 0;

-- 6. Date sanity
SELECT 'silver_orders.order_date out of range' AS failure, order_id, order_date
FROM silver_orders
WHERE order_date < DATE '2015-01-01'
   OR order_date > CURRENT_DATE;

-- 7. Referential integrity (FK -> silver_customers)
SELECT 'silver_orders.customer_id is orphan' AS failure, o.order_id, o.customer_id
FROM silver_orders o
LEFT JOIN silver_customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;


-- -- gold_daily_revenue_by_status ---------------------------------------------

-- 8. Aggregate sanity: gold totals must equal silver totals
WITH g AS (SELECT SUM(revenue) AS total FROM gold_daily_revenue_by_status),
     s AS (SELECT SUM(total_amount) AS total FROM silver_orders)
SELECT 'gold/silver revenue mismatch' AS failure, g.total AS gold_total, s.total AS silver_total
FROM g, s
WHERE ABS(g.total - s.total) > 0.01;

-- 9. No unexpected NULL dates in gold
SELECT 'gold_daily_revenue_by_status.date is NULL' AS failure
FROM gold_daily_revenue_by_status
WHERE date IS NULL;

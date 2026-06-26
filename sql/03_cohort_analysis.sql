-- 03_cohort_analysis.sql
-- Monthly cohort retention in pure SQL (mirrors src/cohort_analysis.py).

WITH order_months AS (
    SELECT
        o.customer_id,
        o.order_id,
        strftime('%Y-%m-01', o.order_purchase_timestamp) AS order_month
    FROM orders o
    WHERE o.order_status != 'canceled'
),

cohort_assign AS (
    SELECT
        customer_id,
        order_month,
        MIN(order_month) OVER (PARTITION BY customer_id) AS cohort_month
    FROM order_months
),

cohort_index AS (
    SELECT
        customer_id,
        cohort_month,
        order_month,
        ( (CAST(strftime('%Y', order_month) AS INTEGER) - CAST(strftime('%Y', cohort_month) AS INTEGER)) * 12
          + (CAST(strftime('%m', order_month) AS INTEGER) - CAST(strftime('%m', cohort_month) AS INTEGER)) ) AS month_index
    FROM cohort_assign
)

SELECT
    cohort_month,
    month_index,
    COUNT(DISTINCT customer_id) AS active_customers
FROM cohort_index
GROUP BY cohort_month, month_index
ORDER BY cohort_month, month_index;

-- To turn this into a retention % matrix, divide active_customers in each row
-- by the active_customers where month_index = 0 for that same cohort_month.
-- (This pivot is easier in Python/Pandas — see src/cohort_analysis.py — or in
-- Excel/Power BI once exported.)

-- 02_rfm_analysis.sql
-- Pure-SQL version of the RFM segmentation (mirrors src/rfm_segmentation.py).
-- Useful to show in interviews as proof you can do this without Pandas too.

WITH order_value AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_purchase_timestamp,
        SUM(oi.price) AS order_total
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.order_status != 'canceled'
    GROUP BY o.order_id, o.customer_id, o.order_purchase_timestamp
),

customer_rfm AS (
    SELECT
        customer_id,
        CAST((julianday((SELECT MAX(order_purchase_timestamp) FROM order_value))
              - julianday(MAX(order_purchase_timestamp))) AS INTEGER) AS recency_days,
        COUNT(*) AS frequency,
        SUM(order_total) AS monetary
    FROM order_value
    GROUP BY customer_id
),

scored AS (
    SELECT
        *,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,   -- lower recency_days = more recent = higher score
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM customer_rfm
)

SELECT
    customer_id,
    recency_days,
    frequency,
    ROUND(monetary, 2) AS monetary,
    r_score,
    f_score,
    m_score,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Lost'
        ELSE 'Needs Attention'
    END AS segment
FROM scored
ORDER BY monetary DESC;

-- 04_kpi_queries.sql
-- A grab-bag of standalone KPI queries useful for the dashboard / a written report.

-- Total revenue, orders, AOV
SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.order_status != 'canceled';

-- Monthly revenue trend
SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS month,
    ROUND(SUM(oi.price), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS orders
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.order_status != 'canceled'
GROUP BY month
ORDER BY month;

-- Top 10 product categories by revenue
SELECT
    p.product_category_name,
    ROUND(SUM(oi.price), 2) AS revenue,
    COUNT(*) AS units_sold
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.order_status != 'canceled'
GROUP BY p.product_category_name
ORDER BY revenue DESC
LIMIT 10;

-- Revenue by customer state
SELECT
    c.customer_state,
    ROUND(SUM(oi.price), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS orders
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.order_status != 'canceled'
GROUP BY c.customer_state
ORDER BY revenue DESC;

-- Repeat purchase rate
WITH order_counts AS (
    SELECT customer_id, COUNT(*) AS n_orders
    FROM orders
    WHERE order_status != 'canceled'
    GROUP BY customer_id
)
SELECT
    ROUND(100.0 * SUM(CASE WHEN n_orders > 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_purchase_rate_pct
FROM order_counts;

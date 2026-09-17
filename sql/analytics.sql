.headers on
.mode column

-- 1. Faturamento total e ticket médio por pedido
SELECT
  ROUND(SUM(line_total), 2) AS faturamento_total,
  ROUND(SUM(line_total) / COUNT(DISTINCT order_id), 2) AS ticket_medio
FROM order_items;

-- 2. Top 10 clientes por faturamento
SELECT c.customer_id, c.name, ROUND(SUM(oi.line_total), 2) AS faturamento
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.name
ORDER BY faturamento DESC
LIMIT 10;

-- 3. Receita mensal usando CTE
WITH monthly AS (
  SELECT substr(o.order_date, 1, 7) AS month, SUM(oi.line_total) AS revenue
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.order_id
  GROUP BY substr(o.order_date, 1, 7)
)
SELECT month, ROUND(revenue, 2) AS revenue,
       ROUND(revenue - LAG(revenue) OVER (ORDER BY month), 2) AS delta_vs_previous
FROM monthly
ORDER BY month;

-- 4. Produtos com maior quantidade vendida
SELECT p.product, p.category, SUM(oi.quantity) AS units
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product, p.category
ORDER BY units DESC
LIMIT 10;

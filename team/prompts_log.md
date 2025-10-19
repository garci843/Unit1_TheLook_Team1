Daniel:
BigQuery SQL Only

**"Generate an SQL query that calculates the monthly revenue and its Month-over-Month (MoM) and Year-over-Year (YoY) growth percentages.

Use CTEs and window functions.

The price is the sale_price from order_items, falling back to retail_price from products.

Use these tables:

`mgmt-467-2500.Assignment_1.order_items` (oi)

`mgmt-467-2500.Assignment_1.products` (p)

`mgmt-467-2500.Assignment_1.orders` (o)

Order the result by month descending and limit it to 10 rows."**


Write a SQL query in BigQuery syntax to calculate the average order value (AOV) for all orders. Use the following tables: order_items with columns like order_id, product_id, and sale_price. products with columns like id and retail_price. orders with columns like order_id, user_id, order_date, and gender. The query should: Join order_items with products using product_id. Use COALESCE(sale_price, retail_price) as the item price. Sum the total item prices per order to get each order’s total value. Then calculate the overall average order value (AOV) as the mean of all order totals. Include a version grouped by month (FORMAT_DATE('%Y-%m', order_date)) as well. Use table references like: mgmt-467-2500.Assignment_1.order_items mgmt-467-2500.Assignment_1.products mgmt-467-2500.Assignment_1.orders


##### Write a SQL query in BigQuery syntax to calculate the gross profit margin for all products and by month. Use the following tables: order_items with columns like order_id, product_id, and sale_price. products with columns like id, retail_price, cost, and category. orders with columns like order_id, order_date, and gender. The query should: Join order_items with products on product_id. Use COALESCE(sale_price, retail_price) as the item price. Calculate revenue as the sum of item prices. Calculate cost of goods sold (COGS) as the sum of product cost. Compute gross profit = revenue - COGS. Compute gross profit margin = gross profit / revenue. Group results by month using FORMAT_DATE('%Y-%m', order_date). Optionally, include filters such as p.category = 'Swim' or o.gender = 'F'. Use fully qualified table references like: mgmt-467-2500.Assignment_1.order_items mgmt-467-2500.Assignment_1.products mgmt-467-2500.Assignment_1.orders Order results by month ascending



Prompt:
Write a SQL query that finds the top 10 products in the "Swim" category by total revenue, grouped by month.

Use two tables:

order_items with columns like product_id, sale_price, and order_date.

products with columns like id, name, retail_price, cost, and category.

The query should:

Join order_items and products on product ID.

Calculate total units sold (COUNT(1)) for each product per month.

Calculate total revenue as the sum of sale_price (or retail_price if sale_price is NULL).

Calculate total margin as revenue minus cost.

Extract the month from order_date (use FORMAT_DATE('%Y-%m', order_date) or equivalent).

Filter to only products in the Swim category.

Group by product ID, name, cost, and month.

Order by revenue in descending order.

Limit the result to the top 10 products by revenue per month.

Use BigQuery syntax and table references like mgmt-467-2500.Assignment_1.order_items.



##### Write a SQL query that calculates monthly gender-segment metrics — revenue, average order value (AOV), and repeat rate — using BigQuery syntax. Use the following tables: order_items with columns like order_id, product_id, and sale_price. products with columns like id, retail_price. orders with columns like order_id, user_id, gender, and order_date. The query should: Create a CTE (ip) to combine order_items with products, using COALESCE(sale_price, retail_price) as item_price. Create another CTE (gender_metrics) that: Groups results by gender and month (derived from order_date using FORMAT_DATE('%Y-%m', order_date)). Calculates: Unique buyers: COUNT(DISTINCT user_id) Revenue: SUM(item_price) AOV (Average Order Value): SUM(item_price) / NULLIF(COUNT(DISTINCT order_id), 0) Orders: COUNT(DISTINCT order_id) Repeat rate: fraction of users with more than one order in that month. Filter the data for gender = 'F'. Return results with columns: gender, month, revenue, AOV, repeat rate, and orders. Order results by month ascending. Use fully qualified table references like: mgmt-467-2500.Assignment_1.order_items mgmt-467-2500.Assignment_1.products mgmt-467-2500.Assignment_1.orders



##### The earlier prompt to calculate Gross Profit Margin implied that you could directly calculate gross profit margin only by grouping monthly order data — but in some cases, gross profit margin should be derived from product-level or order-level data first, then aggregated.


#####
Create an appropriate plot to show the monthly revenue from earlier. dataframe is called results_df_mr




Ethan:
Prompt 1 – Start DIVE analysis project
You’re helping me build a DIVE analytics project using the dataset bigquery-public-data.thelook_ecommerce. Use the DIVE method (Discover, Investigate, Validate, Extend) and tools BigQuery SQL + Python + Plotly + Looker Studio. Generate insights that show growth opportunities and risks, and make recommendations with business value. Be structured and explain your steps clearly.

Prompt 2 – Generate Discover KPIs
Use BigQuery SQL to calculate the top 3 KPIs for ecommerce growth:

Monthly revenue trend with MoM and YoY changes using window functions

Repeat purchase rate per month

Average order value (AOV) per month
Return clean SQL for each metric and explain each KPI briefly.

Prompt 3 – Investigate a category and customer segment
Investigate performance by product category and customer segment. Filter to one product category and one segment and analyze revenue, AOV, and discount behavior. Show which regions or customer characteristics drive performance. Use CTEs and GROUP BY. Return SQL.

Prompt 4 – Investigate Footwear × Male customers
Deep-dive into the Footwear category filtered to male customers. Analyze revenue trends, average discount percentage, and AOV by state or region. Return SQL.

Prompt 5 – Validate misleading insights
Show how an insight could be misleading. Cross-check whether any revenue increase in Footwear is caused by heavy discounting that lowers AOV. Use discount buckets and compare revenue vs AOV. Return SQL.

Prompt 6 – Extend with visualization
Create a SQL query for daily revenue in the last 180 days to use in a Plotly line chart. This will be used in the Extend part of DIVE.

Prompt 7 – Summary recommendations
Write strategist-style recommendations at the end of the analysis. Connect insights to actions and impact. Provide 2–3 recommendations using this structure:
Finding → Implication → Action → Expected impact







Arman: Gemini Prompt Cells

Hypothesis A — Prompt Log
Prompt to Gemini

“Write BigQuery Standard SQL to return the top 10 product categories by revenue in the last 90 days from bigquery-public-data.thelook_ecommerce. Join order_items→orders (for status/date) and products (for category). Filter to Complete orders. Return category, revenue, orders, and AOV (= revenue / distinct orders). Order by revenue desc.”

Key suggestions I used

• Use COALESCE(oi.status,o.status), COALESCE(DATE(oi.created_at),DATE(o.created_at)).

• Compute AOV via SAFE_DIVIDE(SUM(sale_price), COUNT(DISTINCT order_id)).

• Limit to the last 90 days with DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY).


# Hypothesis A — SQL (store results in a Pandas DataFrame)

query_hyp_a = """
WITH filtered AS (
  SELECT
    p.category,
    oi.order_id,
    oi.sale_price
  FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.orders`   o ON oi.order_id   = o.order_id
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.products` p ON oi.product_id = p.id
  WHERE COALESCE(oi.status, o.status) = 'Complete'
    AND COALESCE(DATE(oi.created_at), DATE(o.created_at)) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
),
agg AS (
  SELECT
    category,
    SUM(sale_price) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    SAFE_DIVIDE(SUM(sale_price), NULLIF(COUNT(DISTINCT order_id),0)) AS aov
  FROM filtered
  GROUP BY category
)
SELECT * FROM agg
ORDER BY revenue DESC
LIMIT 10
"""
df_hyp_a = run_bq(query_hyp_a)
df_hyp_a.head(10)
     
Interpretation (2–4 sentences): Top categories by revenue in the last quarter are surfaced here along with order counts and AOV. Use this to select a focus category for the deep dive and to inform the Looker bar chart (Top 5 categories). High AOV with relatively few orders can indicate premium niches; the opposite suggests volume plays.

Hypothesis B — Prompt Log
Prompt to Gemini

“Compare device performance for AOV using both mean and median in thelook_ecommerce. Heuristically attribute device via events within 7 days before the order date (join on user_id). Return device, lines, mean_aov_proxy, median_aov_proxy. Filter to Complete orders in the last 90 days.”

Key suggestions I used

• Join events with DATE_DIFF(f.order_date, e.event_date, DAY) BETWEEN 0 AND 7.

• Median via APPROX_QUANTILES(sale_price, 100)[OFFSET(50)].

• Show counts to judge stability of device comparisons.


# Hypothesis B — SQL

query_hyp_b = """
WITH base AS (
  SELECT
    COALESCE(DATE(oi.created_at), DATE(o.created_at)) AS order_date,
    oi.order_id,
    oi.sale_price,
    o.user_id
  FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.orders` o
    ON oi.order_id = o.order_id
  WHERE COALESCE(oi.status, o.status) = 'Complete'
    AND COALESCE(DATE(oi.created_at), DATE(o.created_at)) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
),
events AS (
  SELECT user_id, device, DATE(event_timestamp) AS event_date
  FROM `bigquery-public-data.thelook_ecommerce.events`
),
joined AS (
  SELECT
    b.order_id,
    b.sale_price,
    ANY_VALUE(e.device) AS device
  FROM base b
  LEFT JOIN events e
    ON e.user_id = b.user_id
   AND DATE_DIFF(b.order_date, e.event_date, DAY) BETWEEN 0 AND 7
  GROUP BY 1,2
)
SELECT
  COALESCE(device, 'Unknown') AS device,
  COUNT(*) AS lines,
  AVG(sale_price) AS mean_aov_proxy,
  APPROX_QUANTILES(sale_price, 100)[OFFSET(50)] AS median_aov_proxy
FROM joined
GROUP BY 1
ORDER BY lines DESC
"""
df_hyp_b = run_bq(query_hyp_b)
df_hyp_b
     
Interpretation (2–4 sentences): If mean and median diverge by device, outliers are influencing the mean. Use median for strategy decisions (e.g., mobile vs. desktop budget mix) and watch the lines column to ensure sufficient sample size by device.

Hypothesis C — Prompt Log
Prompt to Gemini

“Within a chosen category and customer segment, examine whether average discount % correlates with revenue by state in thelook_ecommerce. Compute discount as (retail_price - sale_price)/retail_price. Return state, revenue, orders, avg_discount_pct. Filter to Complete orders in the last 180 days.”

Key suggestions I used

• Segment example: gender = 'F' or age BETWEEN 18 AND 34.

• Aggregate at state level to support a discount-vs-revenue scatter/bubble.

• Use SAFE_DIVIDE to avoid divide-by-zero on retail price.


# Hypothesis C — SQL

DEEP_CATEGORY = "Womens Dresses"
SEGMENT_WHERE = "u.gender = 'F'"

query_hyp_c = f"""
WITH filtered AS (
  SELECT
    u.country,
    u.state,
    p.category,
    oi.order_id,
    oi.sale_price,
    p.retail_price
  FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.orders`   o ON oi.order_id   = o.order_id
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.users`    u ON o.user_id     = u.id
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.products` p ON oi.product_id = p.id
  WHERE COALESCE(oi.status, o.status) = 'Complete'
    AND COALESCE(DATE(oi.created_at), DATE(o.created_at)) >= DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY)
    AND p.category = '{DEEP_CATEGORY}'
    AND {SEGMENT_WHERE}
),
by_state AS (
  SELECT
    country,
    state,
    SUM(sale_price) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    AVG(SAFE_DIVIDE(retail_price - sale_price, NULLIF(retail_price,0))) AS avg_discount_pct
  FROM filtered
  GROUP BY 1,2
)
SELECT * FROM by_state
ORDER BY revenue DESC
"""
df_hyp_c = run_bq(query_hyp_c)
df_hyp_c.head(10)
     
Interpretation (2–4 sentences): If states with higher avg_discount_pct also have higher revenue, this category/segment may be price-elastic there. If revenue is high while discounts are low, consider inventory priority or localized merchandising rather than discounting.





Aditya

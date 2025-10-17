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





Arman:





Aditya

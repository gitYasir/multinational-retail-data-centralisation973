-- Milestone 4 SQL queries

-- Task 1

SELECT country_code AS country, COUNT(country_code) AS total_no_stores
FROM dim_store_details
GROUP BY country_code 
ORDER BY total_no_stores DESC

-- Task 2

SELECT locality, count(locality) AS total_no_stores
FROM dim_store_details
GROUP BY locality 
ORDER BY total_no_stores DESC
LIMIT 7

-- Task 3

SELECT CAST(SUM(product_price * product_quantity) AS DECIMAL(10,2)) AS total_sales,month 
FROM dim_products AS p, orders_table AS ot,dim_date_times AS dt
WHERE p.product_code = ot.product_code AND ot.date_uuid = dt.date_uuid
GROUP BY month
ORDER BY total_sales DESC

-- Task 4

SELECT
  COUNT(*) AS number_of_sales,
  SUM(product_quantity) AS product_quantity_count,
  CASE
    WHEN store_code = 'WEB-1388012W' THEN 'Web'
    ELSE 'Offline'
  END AS location
FROM orders_table
GROUP BY location;

-- Task 5

SELECT
    dsd.store_type,
    ROUND(SUM(dp.product_price * ot.product_quantity)::NUMERIC, 2) AS total_sales,
    ROUND((SUM(dp.product_price * ot.product_quantity)::NUMERIC / d.total * 100)::NUMERIC, 2) AS percentage_total
FROM
    dim_store_details AS dsd,
    dim_products AS dp,
    orders_table AS ot,
    (SELECT ROUND(SUM(dp.product_price * ot.product_quantity)::NUMERIC, 2) AS total
     FROM dim_products AS dp, orders_table AS ot
     WHERE dp.product_code = ot.product_code) AS d
WHERE
    dsd.store_code = ot.store_code AND dp.product_code = ot.product_code
GROUP BY
    dsd.store_type, d.total
ORDER BY
    total_sales DESC;

-- Task 6


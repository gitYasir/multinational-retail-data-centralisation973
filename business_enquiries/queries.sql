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


-- Milestone 4 SQL queries

-- Task 1

SELECT country_code AS country, COUNT(country_code) AS total_no_stores
FROM dim_store_details
WHERE store_code != 'WEB-1388012W'
GROUP BY country_code 
ORDER BY total_no_stores DESC

-- Task 2

SELECT locality, count(locality) AS total_no_stores
FROM dim_store_details
GROUP BY locality 
ORDER BY total_no_stores DESC
LIMIT 7

-- Task 3

SELECT ROUND(SUM(product_price * product_quantity)::numeric,2) AS total_sales,month 
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

SELECT
    ROUND(SUM(ot.product_quantity * dp.product_price)::numeric,2) AS total_sales,
    ddt.year,
    ddt.month
FROM
    orders_table ot, dim_products dp, dim_date_times ddt
WHERE
     ot.date_uuid = ddt.date_uuid AND ot.product_code = dp.product_code AND ot.date_uuid = ddt.date_uuid 
GROUP BY
    ddt.year, ddt.month
ORDER BY
    total_sales DESC;

-- Task 7

SELECT
    SUM(staff_numbers) AS total_staff_numbers,
    country_code
FROM
    dim_store_details
GROUP BY
    country_code
ORDER BY
    total_staff_numbers DESC;

-- Task 8

SELECT
    ROUND(SUM(ot.product_quantity * dp.product_price)::numeric,2) AS total_sales,
    dsd.store_type,
    dsd.country_code
FROM
    orders_table ot, dim_products dp, dim_store_details dsd
WHERE
     ot.store_code = dsd.store_code AND ot.product_code = dp.product_code AND dsd.country_code = 'DE' 
GROUP BY
     dsd.store_type,dsd.country_code
ORDER BY
    total_sales;

-- Task 9

WITH timediff_cte AS (
    SELECT
        TO_TIMESTAMP("timestamp" || month || year || day, 'HH24:MI:SSMMYYYYDD') AS combined_datetime,
        LEAD(TO_TIMESTAMP("timestamp" || month || year || day, 'HH24:MI:SSMMYYYYDD')) OVER (ORDER BY year, month, day) AS next_combined_datetime,
        year,
        month,
        day,
        "timestamp"
    FROM
        dim_date_times
), avg_calculation AS (
    SELECT
        EXTRACT(YEAR FROM combined_datetime) AS year,
        AVG(next_combined_datetime - combined_datetime) AS avg_time_difference
    FROM
        timediff_cte
    GROUP BY
        EXTRACT(YEAR FROM combined_datetime)
)
SELECT
    year,
    jsonb_build_object(
        'hours', EXTRACT(HOUR FROM avg_time_difference),
        'minutes', EXTRACT(MINUTE FROM avg_time_difference),
        'seconds', EXTRACT(SECOND FROM avg_time_difference),
        'milliseconds', EXTRACT(MILLISECOND FROM avg_time_difference)
    ) AS actual_time_taken
FROM
    avg_calculation
ORDER BY
    EXTRACT(HOUR FROM avg_time_difference) DESC,
    EXTRACT(MINUTE FROM avg_time_difference) DESC,
    EXTRACT(SECOND FROM avg_time_difference) DESC,
    EXTRACT(MILLISECOND FROM avg_time_difference) DESC;

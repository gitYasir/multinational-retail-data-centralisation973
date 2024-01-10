-- I was unaware that I had to keep the queries in one place. I already made all the queries for milestone 3, 
-- so I am writing below some examples of the queries I used to complete all the tasks for this milestone.

-- For the tasks that needed the data types to be changed to VARCHAR(?), the following are the 2 queries 
-- I used to find the max length of the data and then cast accordingly.

SELECT MAX(CHAR_LENGTH(store_code)) AS max_length
FROM dim_store_details;

ALTER TABLE dim_date_times
ALTER COLUMN month TYPE varchar(2)
USING month::varchar(2);

-- To cast to the other data types, I used lines 10 to 12, adjusting the table and column names along with the TYPE.

-- I used the following for milestone 3 task 4.

ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(14);

UPDATE dim_products
SET weight_class = 
  CASE 
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
    WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
    WHEN weight >= 140 THEN 'Truck_Required'
  END;

-- When setting columns as primary key:

ALTER TABLE specific_table
ADD PRIMARY KEY (column_name);

-- For creating the foreign key relation to the orders_table using dim_store_details as example

ALTER TABLE orders_table
ADD FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code);
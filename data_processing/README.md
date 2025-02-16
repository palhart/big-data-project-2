# Big-Data-Project-2

## Overview
This project demonstrates a comprehensive data cleaning and processing pipeline for a dataset using PySpark. The pipeline includes the following key steps:

1. **Data Processing and Cleaning**:
   - Handling missing values
   - Removing duplicates
   - Normalizing data formats (timestamp, categorical variables)
   - Validating and cleaning numerical columns
   - Filtering out invalid or irrelevant transactions
   - Generating summary statistics

## Key Challenges
1. **Missing Value Handling**: The dataset did not contain any missing values

3. **Numerical Data Validation**: The pipeline includes checks to ensure that numerical columns (price, quantity, total_amount) contain only non-negative values. This helps to identify and remove any invalid transactions.

## Usage
To run the data pipeline:

1. Ensure you have PySpark installed and configured in your environment.
3. Execute the `data_pipeline.py` script:

```
python data_processing/data_pipeline.py
```

The script will execute the data cleaning and processing pipeline, and print the summary statistics and a sample of the final processed data.

```
Starting cleaning pipeline...
Initial row count before cleaning: 1000000
Checking missing values for column: transaction_id
Checking missing values for column: timestamp
Checking missing values for column: customer_id
Checking missing values for column: customer_name
Checking missing values for column: city
Checking missing values for column: customer_type
Checking missing values for column: product_name
Checking missing values for column: category
Checking missing values for column: price
Checking missing values for column: quantity
Checking missing values for column: total_amount

Missing value counts:
transaction_id: 0
timestamp: 0
customer_id: 0
customer_name: 0
city: 0
customer_type: 0
product_name: 0
category: 0
price: 0
quantity: 0
total_amount: 0
No missing values found.
Skipping remove critical nulls step.
Skipping fill missing values step.
Removing duplicates based on columns: ['transaction_id']
Removed 0 duplicates.
Final row count after cleaning: 1000000
Starting processing pipeline...

Numerical columns summary:
+-------+------------------+---------------+------------------+
|summary|             price|       quantity|      total_amount|
+-------+------------------+---------------+------------------+
|  count|           1000000|        1000000|           1000000|
|   mean| 510.4717896499651|      29.922302|15258.971812960368|
| stddev|280.77937067087254|32.558756872667|20702.528839890252|
|    min|              9.88|              1|              9.88|
|    25%|            273.14|              3|            1174.7|
|    50%|            532.44|             12|            3751.0|
|    75%|            751.12|             56|          23348.91|
|    max|            998.53|            150|         131862.08|
+-------+------------------+---------------+------------------+


Transaction counts by customer type:
+-------------+------+
|customer_type| count|
+-------------+------+
|          B2B|511641|
|          B2C|488359|
+-------------+------+

Data pipeline completed successfully!

Sample of final processed data:
+--------------------+--------------------+-----------+----------------+-------------------+-------------+--------------------+--------------------+------+--------+------------+--------------------+----------+----------------+
|      transaction_id|           timestamp|customer_id|   customer_name|               city|customer_type|        product_name|            category| price|quantity|total_amount|is_valid_transaction|unit_price|transaction_date|
+--------------------+--------------------+-----------+----------------+-------------------+-------------+--------------------+--------------------+------+--------+------------+--------------------+----------+----------------+
|TX_00024ec3-c398-...|2024-05-09 08:06:...|       6574|    Todd Cochran|   New Kennethville|          B2B|  Fiction Product_15|     Books > Fiction| 91.94|      34|     3125.96|                true|     91.94|      2024-05-09|
|TX_0002b33d-d1a2-...|2024-02-08 23:57:...|       9765|     Brenda Ward|      Stephanieview|          B2B|Personal Care Pro...|Health & Personal...|229.23|      39|     8939.97|                true|    229.23|      2024-02-08|
|TX_0002c6b1-dfed-...|2024-09-29 13:24:...|       6833|  Todd Alexander|       Cassidyburgh|          B2C|   Fiction Product_9|     Books > Fiction|463.95|       3|     1391.85|                true|    463.95|      2024-09-29|
|TX_00035645-287a-...|2024-01-22 17:24:...|        784|Michael Mitchell|         Port Andre|          B2B|   Comics Product_14|      Books > Comics| 67.75|      99|     6707.25|                true|     67.75|      2024-01-22|
|TX_0003f3a3-eae5-...|2024-10-10 04:50:...|       3848|   Javier Finley|South Elizabethfurt|          B2B|  Skincare Product_9|Health & Personal...|744.75|      28|     20853.0|                true|    744.75|      2024-10-10|
+--------------------+--------------------+-----------+----------------+-------------------+-------------+--------------------+--------------------+------+--------+------------+--------------------+----------+----------------+
only showing top 5 rows

```
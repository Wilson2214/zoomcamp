-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-1-410619.ny_taxi.external_green_tripdata` 
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://mage-zoomcamp-green-taxi/nyc_green_2022_manual/*.parquet']
);

-- Create a non partitioned, non-clustered table from external table
CREATE OR REPLACE TABLE zoomcamp-1-410619.ny_taxi.green_tripdata_non_partitoned AS
SELECT * FROM zoomcamp-1-410619.ny_taxi.external_green_tripdata;

-- Question 1: count records
SELECT count(*) FROM `zoomcamp-1-410619.ny_taxi.external_green_tripdata`;
-- 840,402 (also confirmed via ingestion by Mage)

-- Question 2: How much estimated data will be processed
SELECT COUNT(DISTINCT(PULocationID)) FROM zoomcamp-1-410619.ny_taxi.external_green_tripdata;
-- Per validator: This query will process 0 B when run.

SELECT COUNT(DISTINCT(PULocationID)) FROM zoomcamp-1-410619.ny_taxi.green_tripdata_non_partitoned;
-- Per validator: This query will process 6.41 MB when run.

-- Question 3: How many records have a fare_amount of 0?
SELECT COUNT(*) FROM zoomcamp-1-410619.ny_taxi.external_green_tripdata WHERE fare_amount = 0;
-- 1622

-- Question 4: What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)

-- Partition by pickup date because a filter will allow us to select fewer sets of data
-- Cluster by PULocationID because this will pre-order results by these ids
CREATE OR REPLACE TABLE zoomcamp-1-410619.ny_taxi.green_tripdata_partitoned
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PULocationID AS
SELECT * FROM zoomcamp-1-410619.ny_taxi.green_tripdata_non_partitoned;

-- Question 5
SELECT DISTINCT(PULocationID)
FROM zoomcamp-1-410619.ny_taxi.green_tripdata_non_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';
-- Per validator: This query will process 12.82 MB when run.

SELECT DISTINCT(PULocationID)
FROM zoomcamp-1-410619.ny_taxi.green_tripdata_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';
-- Per validator: This query will process 1.12 MB when run.

-- Question 6: Where is the data stored in the External Table you created?
-- GCP Bucket
-- Per lecture: 'the data itself is not inside big query, it's in an external system such as google 
-- cloud storage'
-- Per Google: 'An External Table is a table that operates like a standard Google BigQuery table 
-- since its table metadata and the table schema are both stored in Google BigQuery storage, but, 
-- the data itself resides in the external source'

-- Question 7: It is best practice in Big Query to always cluster your data:
-- TRUE
-- Clustering addresses how a table is stored so it's generally a good first option for improving query performance. You should therefore always consider clustering given the following advantages it provides:
-- If your queries commonly filter on particular columns, clustering accelerates queries because the query only scans the blocks that match the filter.
-- If your queries filter on columns that have many distinct values (high cardinality), clustering accelerates these queries by providing BigQuery with detailed metadata for where to get input data.
-- Clustering enables your table's underlying storage blocks to be adaptively sized based on the size of the table.
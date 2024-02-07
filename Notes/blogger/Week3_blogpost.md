Data Engineering ZoomCamp Week 3

dlt Workshop
This week started with a workshop on dlt or "data load tool". This is an open source library which enables data engineers to build data pipelines faster and better. The goal of dlt is to automate the tedious parts of data ingestion like loading, schema managment, data type detection, and scalability. This is important, because in essence "a data engineer's main goal is to ensure data flows from source systems to analytical destination". The process of this data flow is called an ETL or extracting, transforming (including normalizing), and loading.

The highlight of this workshop was the discussion of a problem many data engineers, including myself, have faced. That problem is managing memory. ETL pipelines always need to work, but can run into issues because the size of the data is not always known. If we build a pipeline that loads a full dataset, it could potentially crash if the source data becomes too large. It is important then to be able to extract data without hitting hardware limits in relation to memory. The best option to manage memory issues is to control the maximum amount of memory used by streaming the data. In Python, this can be done with generators. Instead of defining a function that returns all data from the source, we define a generator which allows us to yield each row as we get the data without collecting it into memory. Implementing a generator with dlt allows for more efficient data processing and limits memory impacts.

Data Warehousing with BigQuery

Data Warehouses are an OLAP solution used for reporting and data analysis. One can think of a data warehouse as a final storage area for a number of data sources. This can include raw data, metadata, and summary data. BigQuery is a serverless data warehouse that allows data warehousing to be scalable and highly available. It also includes built-in features like machine learning and business intelligence. A major component of Big Query that we discussed this week was Partitioning and Clustering which are features that can reduce cost and improve speed

Partitioning

Paritioning 'involves dividing a table into segments, called partitions, that make it easier to manage and query your data' per [Google](https://cloud.google.com/bigquery/docs/partitioned-tables). By dividing this table you can improve query performance and reduce costs by processing less data per query. For instance, if you partition by month and write a query that only requires one month of data to be analyzed, only that partitioned will be analyzed in the query. This will be much faster and more cost effective than searching the entire dataset for records falling within that month.

Clustering

Clustering on the other hand is an additional feature which can also reduce cost and time to run queries. Users can define a feature to cluster on which groups data with these similar features together into blocks. Queries that filter or aggregate by a clusterd column only need to scan the relevant blocks which reduces cost and time. For queries that commonly use filters or aggregation, clustering can be extremely beneficial. Clustering is also more beneficial than partitioning when partitioning results in a small amount of data per partition.

Tables with data size less than 1 GB don't show significant improvement with partitioning and clustering.

Homework

As mentioned in previous weeks, a major roadblock to building our data pipeline was schema. Through the first two weeks of class, we utilized Python within Mage to build a pipeline that reads files from an external location (API) into Pandas, transforms the data and sets the schema, than loads that data into a Google Cloud Bucket. This week, instead of using csv files from our source system, we were tasked with using parquet files. Although Python and Pandas have functionality to interact with parquet, I ran into a number of issues related to schema. In particular this seemed to have something to do with date features in the dataset. Ingesting a parquet file with Pandas in Python resulted in dates being read as type 'datetime[ns]'. I was then able to take this parquet file and export it to a Google Cloud Bucket without issue. The problem arose when I attempted to create an external table in BigQuery with:

```
CREATE OR REPLACE EXTERNAL TABLE `{project-id}.ny_taxi.external_green_tripdata` 
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://{bucket}/nyc_green_2022_manual/*.parquet']
);
```

Ingestion of this pandas datetime object resulted in creating a BIGINT integer datatype. The benefit of parquet is that it stores metadata about the schema of the parquet file. What was interesting is that the schema correctly identifies these dates as datetype, but Big Query does not understand them as anything but an integer. As I move forward in this course, I will know that this issue exists and will need to find a proper workaround for it.
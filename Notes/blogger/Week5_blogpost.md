Data Engineering ZoomCamp Week 5

Week 5 of the Data Engineering ZoomCamp was focused on batch data processing with Spark. Analytics engineering as a role generally sits between data engineering and data analysis. The goal of analytics engineering is to introduce good software engineering practices to the efforts of the data analysts and data scientists. To learn more about the Data Engineering ZoomCamp, sign up for the next cohort, or walk through the videos at your own pace, check out the Data Talks website. My code and notes will be available on GitHub.

Batch Processing

What is batch processing? [flesh out more]
Majority (80% or more) of ETL jobs / processing jobs tend to be batch jobs
Can easily setup batch processing with Python scripts, SQL, Spark, or other frameworks.
Typically would use an orchestrator to manage these scripts

Advantages of Batch:
- convenience and ease to manage
- can quickly retry scripts if there was an issue
- scalability based on input size requirements
Disadvantages:
- Delay in getting data to final system

Spark

What is spark? [flesh out more]
A multi-language data processing engine (java, scala, python, and R wrappers). Pyspark is very popular way to write a spark job

When to use spark?
- Often used when we have a data lake or other unoptimized data warehouse that cannot be easily queried with SQL

Deploying Spark
Data Engineering ZoomCamp Week 5

Week 5 of the Data Engineering ZoomCamp was focused on batch data processing with Spark. I have a lot of familiarity with batch processing and Spark as these are the main tools my current organization uses to ingest and process data. I was interested in learning more about Spark internals, RDDs, and other topics this week though to improve my comprehension. To learn more about the Data Engineering ZoomCamp, sign up for the next cohort, or walk through the videos at your own pace, check out the Data Talks website. My code and notes will be available on GitHub.

Batch Processing

Batch processing is a method to periodically run data processing jobs to ingest, transform, and load data. These jobs or batches can be run on a subset of data (usually when new data added to a source system) or to manipulate full accumulated data in an ingested raw table. Interestingly, the majority (80% or more) of ETL jobs and processing jobs tend to be batch jobs. I have seen this in my own work as 100% of jobs that I work with are batch jobs. I think this is because batch jobs tend to make repetitive tasks more efficient. We can quickly trigger a script or set of scripts to process data rather than rely on streaming to constantly update data. Additionally, this is likely due to the use cases of data that I work with. Often times new data is supplied at a longer frequency (weeks to months) rather than up to the minute or second. Knowing that we might only have new data once per week, it would not be beneficial to use compute resources to monitor a source system or queue to run processing. Finally, batch processing can be easily setup with Python scripts, SQL, Spark, or other frameworks. Typically we would use an orchestrator to manage these scripts. For instance, I currently use a combination of PySpark, Python, and R scripts to batch process data and store its outputs to a Data Warehouse.

Overall, the advantages of Batch are:
- Convenience and ease to manage
- Ability to quickly retry scripts if there was an issue. It also has a good audit trail and logging if a script does fail.
- Scalability based on input size requirements. It can be ideal for processing large volumes of data as you are not processing individual records.
- Lower costs as compute resources only need to be spun up on an as-needed basis. Scripts can also be run during less-busy hours to secure lower pricing.

The main disadvantage is:
- Delay in getting data to final system meaning that data can be out of date. Again this is only an issue if your end result requires near real time access to data

Due to these few disadvantages, batch processing is often chosen.

Spark 101

Spark is a multi-language data processing engine framework that manages the processing of data across parallel nodes. It operates as an API by splitting tasks up and performing data transformations, then combining back to a final state. It supports wrappers in languages such as java, scala, python, and R to easily write SparkSQL code to be used by the processing engine. Pyspark is very popular way to write a spark job and is used in this course as well as in my personal use with Spark. I also have extensively used SparkR and sparklyr which are two wrappers for spark in R. sparklyr in particular is useful for data processing as we can use dplyr style code and piping to manipulate data efficiently. There are two scenarios in which Spark is particularly useful. When the data to be processed is too large for the available computing and memory resources or as an alternative when one wants to accelerate a calculation by using several machines within the same network. In both cases, a major concern is to optimise the calculation time of a Spark job.

The easiest way to explain what Spark does is with an example. I found (this example about counting candies)[https://medium.com/uncle-data/distributed-data-processing-simplified-e691e2159508] to be the  most effective. The question is, what is an efficient way to count a large quantity of candies?

- If the portion is small, you can just count one by one.
- If the portion is large thouhg, you may want to ask others to count a subset. These counts can then be provided back to me where I sum up the results. This can be seen as parallel processing.

The same process can be used with transforming data. If I have a large set of data, I can use parallel computing to process transformations on subsets of the data, then gather the results at a central node to provide an output. This is why Spark is often used when we have a data lake or other unoptimized data warehouse that cannot be easily queried with SQL

Again, Spark allows us to parallelize computations across executors. We can think of an executor as a single virtual machine. A virtual machine has a CPU with a set number of cores where work is actually performed and an amount of memory to store data. Each core can be considered a slot where a task can be performed. In spark, tasks are divided among executors and their cores. When work is complete, the outputs of these tasks are collected at a central point called the driver which also has a CPU and a set amount of memory. Because this driver is collecting the transformed (and likely now smaller set of data) it does not need to be as large as it would if we were simply performing a task on a single virtual machine. The spark driver also orchestrates the execution of the processing and distribution among spark executors.

There are two main architectures that we can use with spark
Single Node or Local Mode: This is our most common application when developing a process. It allows us to use spark on a single virtual machine. This machine likely has 8-32 cores. Spark will set aside a set amount of memory and cores as a driver and divide the remaining memory and cores to be executors. Spark SQL commands can then be run and collected taking advantage of Spark without the need to spin up multiple virtual machines.
Standard: This is most often used in production. In this case, 1 driver virtual machine is spun up in addition to one or more executor virtual machines. This allows us to utilize more computing power and memory to complete tasks but requires more optimization to prevent cost overruns unused computing power.

Compute Planning in Spark

There are two compute functions Spark performs; transformations and actions. Transformations (like select or filter) change the data and actions return data. This is best understood in terms of lazy evaluation. Lazy evaluation is a trick for large data processing to optimize computations. Lazy evaluation creates a plan of computations but does not trigger actual processing until data is required to be returned. Spark SQL uses this idea to create a plan to perform transformations. This is why Spark code is so fast until the time of getting the output. For instance we may create a new attribute, join two tables, and then group by and summarize data. This will create plan to generate a final output, but with no data actually changed or returned. If we decide to print this data, save it to a file, or even view a subset of data though, we have to perform an action. An action actually executes the Spark SQL plan and formalizes the data transformations across the nodes available. Actions generally come in the form of calling a collect command to bring the data to the main node or driver. This also occurs when we call write or cache commands or even when we look to just see the first few records of a table with a head call.

As described, transformations of data are planned computations performed across excutors and data is stored in partitions of an RDD. This means that individual executors get a portion (partition) of the data to work with. Some transformations allow executors to work with just the data on its partition while other transformations require data to be shuffled across executors. There are two types of transformations; narrow and wide.

- Narrow Transformations are those where the data required to compute records will reside in a single partition. Examples include select, drop, and where statements. For example, if we wanted to drop a column across the dataset, each executor could simply drop that column without needing to work with each other.
- Wide Transformations are those where the data required to compute records resides in many partitions of the data. Examples include distinct, group by, and order by. For example, if I wanted to group by a column, I would need to group by on each excutor and partition. When I go to collect, this will cause a shuffle of the data as we will then need to group by at the driver level.

Wide transformations and shuffles are the most computationally expensive and should be avoided if unnecessary. If they are necessary (often times this is the case), you should optimize the spark configuration so that there are the right number of executors and partitions.

Running Spark

As mentioned previously, Spark is a data processing engine with wrappers written in other languages. Although we could write specific Spark SQL commands to perform our transformations, we can instead use a more familiar programming language like R or Python. If we are using one of these wrappers we have to initially create a spark session. A spark session object is the primary entry point for Spark applications. In Python, we create a spark session with:

```
spark = SparkSession.builder \
    .master("local[*]") \
    .getOrCreate()
```

Similarly in R we could run:

```
sc <- sparklyr::spark_connect(method = 'local')
```

You'll notice in both instances, we are using local mode to create this session. As described above this means we are using our local compute to run spark instead of a cluster of compute resources. You can adjust spark configuration settings when setting up a session, including setting a particular method. Once a session is created though, we can use PySpark or SparkR commands to manipulate data and use the Spark engine to process these commands.

Finally, spark is best used in the cloud with something like Databricks (spark native) or Google Cloud Platform. We can create a specicific Spark processing node which allows us to run in local mode or create a cluster of nodes to run a production processing job. We can then create a job based on a PySpark or SparkR script and submit it to this compute resource where it will be run.

Additional Information

[This article](https://towardsdatascience.com/6-recommendations-for-optimizing-a-spark-job-5899ec269b4b) was a massive help in understanding Spark and how to optimize and is used in the above article.
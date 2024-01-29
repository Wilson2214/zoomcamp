Data Engineering ZoomCamp Week 2
Week 2 of the Data Engineering ZoomCamp was focused on Orchestration with Mage. In the past, I have worked with Orchestration tools including Airflow and the jobs functionality in Databricks. I am excited to learn more about an open-source tool like Mage and how it stacks up against these other tools. To learn more about the Data Engineering ZoomCamp, sign up for the next cohort, or walk through the videos at your own pace, check out the Data Talks website. My code and notes will be available on GitHub.
Orchestration
Extraction, transformation, and loading between data sources are the main components of data engineering. Automation is key to making these processes more efficient and repeatable. Per the coursework,
"Orchestration is a process of dependency management, facilitated through automation. The data orchestrator manages scheduling, triggering, monitoring, and even resource allocation."
In my time as a data engineer, orchestration has been the most vital component of my job. Being able to quickly update datasets based on new input data is vital to the success of downstream models and other resources. Orchestration is the key to the entire process of building data engineering pipelines. As laid out in the coursework, a good orchestration tool must handle:
Workflow Management
Automation
Error Handling and Recovery
Monitoring and Alerting
Resource Optimization
Observability
Debugging
Compliance and Auditing

Mage
One tool that does handle all of the above is called Mage. This course allowed me to interact with this orchestrator for the first time, but it is quite similar to other tools I've worked with in the past. The general idea is to build a flow of scripts to ingest, manipulate, and store data.
In Mage, these scripts are called Blocks. Pipelines are composed of blocks that can load, transform, or export data and can be written in numerous languages (Python, SQL, etc.). There are additional blocks for conditionals, sensors, webhooks, and more. It also allows for working within GUI or using other tools like VSCode. Blocks are managed and orchestrated via Mage and blocks can be re-used across pipelines. This is my favorite feature of Mage, as multiple pipelines can reuse the same code efficiently! In the GUI, you can also easily create blocks with pre-defined functionality and simply update them with your arguments (i.e. import from GCP with just a few keystrokes.)
Another benefit of Mage is that all development of pipelines and associated information is in code. In our use case, we spin up a docker network with Mage and Postgres. We can then use the Mage GUI or directly edit files in VSCode to build our pipeline. Again this is all stored as code for quick deployments. The final feature of Mage that I find useful is the @test decorator. We can create a test to confirm that something like pre-processing went as planned and that we do not have errors in our dataset. 
Orchestration and Schema
This week's coursework did bring up the idea of schema and its importance again. In the first week, we had to automatically define our schema with a Python function. This week we are manually defining our data schema. In either instance though, schema was the most important entrypoint into the ETL process. Defining your schema should always be the first step when analyzing your data. It also shows one of the difficulties of data engineering. If your schema changes over time - especially your source schema which you may not have control over - you will likely run into major issues in your pipeline.
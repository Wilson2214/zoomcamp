Data Engineering ZoomCamp Week 2

Week 2 of the Data Engineering ZoomCamp will be focusing on Orchestration with Mage. In the past I have worked with Orchestration tools before such as Airflow and the jobs functionality in Databricks. I am excited to learn more about an open source tool like Mage and how it stacks up against these other tools. If you want to learn more, feel free to sign up for the next cohort or walk through the videos at your own pace. My code and notes will be available on GitHub.

Docker containerization to run Mage and Postgres

Orchestration:

ETL between data sources is the main component of data engineering. Automation is key to make these processes either.

"Orchestration is a process of dependency management, facilitated through automation. The data orchestrator manages scheduling, triggering, monitoring, and even resource allocation."

Orchestration is the key to the entire process of building data engineering pipelines.

A good orchestrator handles
- workflow management
- automation
- error handling and recovery
- monitoring, alerting
- resource optimization
- observability
- debugging
- compliance and auditing

Mage

Pipelines are composed of blocks which can load, transform, or export data and can be written in numerous languages (Python, SQL, etc.). There are additional blocks for conditionals, sensors, webhooks, and more. It also allows for working within GUI or using other tools like VSCode. Blocks are managed and orchestrated via Mage and blocks can be re-used across pipelines.

One benefit of Mage is that all development of pipelines and associated information is in code. In our use case, we spin up a docker network with Mage and Postgres. We can then use the Mage GUI or directly edit files in VSCode to build our pipeline. Again this is all stored as code for quick deployments.

Note: in this case we are manually defining our data schema (we did this automatically in week 1 so we could build that in here). This shows one of the difficulties of data engineering (schema drift, etc.)

What I find beneficial about Mage is the @test decorator. We can create a test to confirm that something like pre-processing went as planned and we do not have errors in our dataset. I also really like the build functionality in the GUI. You can easily create blocks with pre-defined functionality and simply update them with your arguments (i.e. import from GCP with just a few key strokes.)
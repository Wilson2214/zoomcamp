Data Engineering ZoomCamp Week 1
In an effort to learn some industry standard tools and continue to upskill in my Data Engineering journey, I have decided to enroll in a free data engineering boot camp called the DE Zoomcamp presented by DataTalks.Club. It's an exciting opportunity to advance my skills in cloud computing, containerization, SQL, python, ETL, and other data engineering skills. In particular, I am excited to learn about industry workflow orchestration tools and dive deeper into stream processing of data. This blog will document some of the components of the course that I find the most interesting and any challenges I may face. If you want to learn more, feel free to sign up for the next cohort or walk through the videos at your own pace. My code and notes will be available on GitHub.

Course Setup
One of the issues with working on a variety of projects within Python is packages interfering with one another. When I first started the course setup I jumped into installing packages and running code which resulted in failing to get pgcli to work. I decided to take a step back and create a virtual environment for Python, which should have been my first step. Thankfully, a virtual environment is easy to setup:
# Create a virtual environment named zoomcamp_venv
python3 -m venv zoomcamp_venv
# Activate venv by running activate from your current directory
. zoomcamp_venv/bin/activate
This virtual environment can be used from your command line or within Visual Studio. Additionally, if you already have a Jupyter Notebook running, you can switch it to your virtual environment with:
# Install venv for Jupyter notebook
python3 -m ipykernel install --name=zoomcamp_env
Once my virtual environment was set up, I had no additional package issues. The only additional setup that I had to deal with was creating my Github repository. Again, I should have started with a remote repo, but I eagerly jumped into creating files. It was easy enough to connect my local directory to a remote repository (just make sure your repo and directory have the same name):
# Create blank remote repository in GitHub, then from command line run
git init
git add .
git commit -m "First commit"
git remote add origin <remote url>
git push origin main
git branch --set-upstream-to=origin/main main
Before running the above commands, I would also recommend creating a .gitignore file so as not to upload any csv or database files which can be too large to manage with GitHub.
Containerization: Docker
After setup, Week 1 jumps right into containerization with Docker. Although I have used Docker in the past, it was nice to get a refresher on how to set up and run through the command line. Similar to a virtual environment, Docker containers provide a decoupled environment for an application to run. In our case, we are creating containers to create a Postgresql database, interact with the data via Pgadmin, and run python scripts with Python 3.9. The course details the various methods that allow you to create and work with these containers.
Docker Run
At the most basic level, you can run docker from the command line with an existing Docker image. For instance if you run:
docker run -it ubuntu bash
A docker container with Ubuntu will be created and will begin to run from your command line with the entrypoint of bash. You can then run bash commands in this container. There are thousands of containers that can be selected to run with a variety of environments.
Dockerfile
Instead of just using a generic docker image though, you can instead build your own with a Dockerfile. This file allows you to start with a basic Docker image (i.e. Python 3.9.1) and incorporate additional packages and an entrypoint. For example, say we want a container with Python that has Pandas pre-installed for data analysis. We can create a Dockerfile:
FROM python:3.9.1
RUN pip install pandas
ENTRYPOINT ["bash"]
Then build with Docker:
docker build -t test:exampletag .
Which will create this container. After running it we will then have a Python environment with pandas pre-installed. Using this information we then have the ability to create custom images with various inputs for use in our applications. This includes creating images to run Python or setup and manage a Postgresql database.
Docker-networks
Building upon the idea of creating individual containers with custom environments is the idea of docker-networks. If we individually run docker containers, they have no way of interacting with each other. For example, if we have setup a database in one container and Python in another, we will not be able to use pandas to manipulate the data. Docker networks allow us to coordinate and run multiple containers as one. We do this by creating a docker network, then running our various containers and mapping them to the network:
# Create docker network
docker network create pg-network

# Create postgres docker (connected via network)
docker run -it \
    --network=pg-network \
    --name pg-database \
    postgres:13

# Create pgadmin docker (connected via network)
docker run -it \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
In the above code, you will see that each container is given a unique name and is associated with the network.
Docker Compose
Putting everything together, we can use docker-compose to define and run a docker network without having to individually run a number of commands with Docker. Docker compose uses a yaml file to define the docker run commands. Once written, we use `docker-compose up` to spin up the containers.
Docker Desktop
Although not covered in this coursework, I find Docker Desktop to be especially useful in managing containers and images. Docker Desktop allows you to see which containers are created and if they are running or idle. It also provides you the opportunity to clear space by deleting unused images and containers.
Pandas and SQL
Working through the Docker portion of Week 1 of the Zoomcamp includes creating a Python script to ingest csv data, setting up a Postgresql database to store the data, and using Python with Pandas as well as Pgadmin with SQL to interact with the data. This portion of the coursework was straightforward, but it was interesting to see the variety of options one has to interact with and manipulate data. It also brought up an extremely important component of data ingestion and manipulation: schema. I often run into issues with data analysis simply due to incorrect schema. In this case, dates were ingested as text and had to be corrected to date before loading into the database. I think as a data engineer it is vital to understand the data we are ingesting so as to have the right schema before moving forward
Infrastructure as Code: Terraform
Terraform is a service that runs on your local machine that allows us to manage configuration files to maintain an ideal provisioning state for environments. It allows us to build, change, and manage infrastructure in a safe and consistent manner. Infastructure as code is managed from a main.tf file. The basic execution steps of this file are:

1. `terraform init`: Initialize terraform and connect to the cloud provider we are working with.
2. `terraform plan`: Creates an execution plan (i.e. what resources are we going to provision)
3. `terraform apply`: Applies changes from plan defined in main (i.e. creates the actual resource like a bucket)
4. `terraform destroy`: Remove everything defined in main (i.e. remove the actual resource like a bucket)

One thing to note here is how to use credentials. We can use Google authentification for our main account to simply login with:

gcloud auth application-default login

Or we can create a key and store the json file locally. We then need to set our environment variable to point to this downloaded key:

export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

If we use a variables.tf file though, we can hardcode this authentication key with:
variable "credentials" {
  description = "My Credentials"
  default     = "my_creds.json"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}

#dezoomcamp
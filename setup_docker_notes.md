Create docker network
'''
docker network create pg-network
'''

Create postgres docker (connected via network)
'''
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v /Users/davewilson/Documents/zoomcamp/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13
'''

Create pgadmin docker (connected via network)
'''
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
'''

Now that the above are created, can also manage from docker desktop with names specified

To run our python script with inputs can use the following

'''
#Data now hosted on github
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
'''

Instead of running file directly, can build a docker image to run the file. Build new docker image from Dockerfile:
'''
docker build -t taxi_ingest:v001 .
'''

Then run with docker:
'''
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url=${URL}
'''

Instead of individually running the above multiple times, use docker-compose with a docker-compose.yaml file to network two defined docker images:

'''
docker-compose up
'''

For homework (after running docker-compose up), we would have to update the URL to the correct file (2019-09), then we can change the table name to green taxi trips.
'''
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table_name=green_taxi_trips \
        --url=${URL}
'''
The problem is, there is a different schema than yellow trips. For quick analysis I have instead used jupyter to manually upload.
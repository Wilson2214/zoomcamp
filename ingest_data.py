#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from time import time
from sqlalchemy import create_engine
import argparse
import os

def main(params):

    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv'

    # Download the csv file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    # Connect to postgres to help generate schema in postgres language
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        t_start = time()
        
        df = next(df_iter)
        
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=table_name, con=engine, if_exists='append')
        
        t_end = time()
        
        print('inserted another chunk..., took %.2f second' %(t_end - t_start))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    # user
    parser.add_argument('--user', help='username for postgres')
    # password
    parser.add_argument('--password', help='password for postgres')
    # host
    parser.add_argument('--host', help='host for postgres')
    # port
    parser.add_argument('--port', help='port for postgres')
    # database name
    parser.add_argument('--db', help='database name for postgres')
    # table name
    parser.add_argument('--table_name', help='name of table to write results to')
    # url of the csv
    parser.add_argument('--url', help='url for postgres')

    args = parser.parse_args()

    main(args)
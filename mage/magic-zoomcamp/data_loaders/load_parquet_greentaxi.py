import io
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    base_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-'
    li = []
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    
    for fn in months:
        url = base_url + fn + '.parquet'

        df = pd.read_parquet(url)
        
        # Provide a parquet partition
        # df['month'] = fn

        li.append(df)

    return(pd.concat(li,axis=0,ignore_index=True))

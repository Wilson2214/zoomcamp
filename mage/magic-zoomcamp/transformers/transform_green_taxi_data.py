import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # Check number of rows matching this criteria
    print('Rows with zero passengers:', data['passenger_count'].isin([0]).sum())
    print('Rows with no distance:', data['trip_distance'].isin([0.0]).sum())
    print('Original values in VendorID:', data['VendorID'].unique())
    print('Original column names:', data.columns)

    # Create pickup date column
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    print(data['lpep_pickup_date'].nunique())
        
    # Convert to snake case
    data.columns = (data.columns
                 .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                 .str.lower()
    )

    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

    # Homework Question 4
    print('Final values in vendor_id:', data['vendor_id'].unique())
    print('Final column names:', data.columns)

    return data

@test
def test_passengers(output, *args):
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'

@test
def test_distance(output, *args):
    assert output['trip_distance'].isin([0.0]).sum() == 0, 'There are rides with zero distance travelled'

@test
def test_column(output, *args):
    assert output.columns.isin(['vendor_id']).any(), 'There is no column named vendor_id'
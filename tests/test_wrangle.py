import pandas as pd
import pytest
import sys
import os

# Add the project root to the Python path to allow importing from `src`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.wrangle import clean_api_data

@pytest.fixture
def raw_api_dataframe():
    """Creates a sample raw DataFrame mimicking the SpaceX API structure for testing."""
    data = {
        'flight_number': [1, 2],
        'name': ['FalconSat', 'DemoSat'],
        'date_utc': ['2006-03-24T22:30:00.000Z', '2007-03-21T01:10:00.000Z'],
        'rocket': ['5e9d0d95eda69955f709d1eb', '5e9d0d95eda69955f709d1eb'],
        'launchpad': ['5e9e4502f5090995de566f86', '5e9e4502f5090995de566f86'],
        'payloads': [
            [{'mass_kg': 20, 'orbit': 'LEO'}],
            [{'mass_kg': None, 'orbit': 'LEO'}] # Test missing payload mass
        ],
        'cores': [[{
            'core': {'serial': 'Merlin1A'},
            'flight': 1,
            'gridfins': False,
            'legs': False,
            'reused': False,
            'landing_success': False
        }], [{
            'core': {'serial': 'Merlin2A'},
            'flight': 1,
            'gridfins': True,
            'legs': True,
            'reused': False,
            'landing_success': True
        }]]
    }
    # Create a dummy 'name' column for launchpad lookup, as in the wrangle script
    df = pd.DataFrame(data)
    df.loc[df['launchpad'] == '5e9e4502f5090995de566f86', 'name'] = 'Kwajalein Atoll'
    return df

def test_clean_api_data(raw_api_dataframe):
    """Tests the clean_api_data function from src/wrangle.py."""
    cleaned_df = clean_api_data(raw_api_dataframe)

    # Test 1: Check if the output is a pandas DataFrame
    assert isinstance(cleaned_df, pd.DataFrame)

    # Test 2: Check if the 'class' column was created correctly (False -> 0, True -> 1)
    assert 'class' in cleaned_df.columns
    assert cleaned_df['class'].tolist() == [0, 1]

    # Test 3: Check if missing PayloadMass was filled with the mean (should be 20.0)
    assert not cleaned_df['PayloadMass'].isnull().any()
    assert cleaned_df.loc[1, 'PayloadMass'] == 20.0

    # Test 4: Check if the final columns are as expected
    expected_cols = ['flight_number', 'Date', 'BoosterVersion', 'PayloadMass', 'Orbit',
                     'LaunchSite', 'Outcome', 'Flights', 'GridFins', 'Reused', 'Legs', 'class']
    assert all(col in cleaned_df.columns for col in expected_cols)
    assert len(cleaned_df.columns) == len(expected_cols)

    # Test 5: Check number of rows
    assert len(cleaned_df) == 2
import pandas as pd
import numpy as np
import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.features import create_features, split_and_scale_data

@pytest.fixture
def sample_clean_dataframe():
    """Creates a sample cleaned DataFrame for feature engineering tests."""
    data = {
        'Orbit': ['LEO', 'GTO', 'LEO'],
        'LaunchSite': ['CCAFS', 'VAFB', 'CCAFS'],
        'GridFins': [True, False, True],
        'Reused': [False, False, True],
        'Legs': [True, False, True],
        'PayloadMass': [500, 8000, 500],
        'Flights': [1, 1, 2],
        'class': [1, 0, 1]
    }
    return pd.DataFrame(data)

def test_create_features(sample_clean_dataframe):
    """Tests the one-hot encoding logic in the create_features function."""
    features_df = create_features(sample_clean_dataframe)

    # Test 1: Original categorical columns should be dropped
    assert 'Orbit' not in features_df.columns
    assert 'LaunchSite' not in features_df.columns

    # Test 2: New one-hot encoded columns should exist
    assert 'Orbit_LEO' in features_df.columns
    assert 'LaunchSite_CCAFS' in features_df.columns
    assert 'Reused_True' in features_df.columns

    # Test 3: The number of rows should remain unchanged
    assert len(features_df) == len(sample_clean_dataframe)

def test_split_and_scale_data(sample_clean_dataframe):
    """Tests the data splitting and scaling logic."""
    features_df = create_features(sample_clean_dataframe)
    X = features_df.drop('class', axis=1)
    Y = features_df['class']

    # Using a 33% test split on 3 rows will result in a 2/1 train/test split
    X_train, X_test, Y_train, Y_test, scaler = split_and_scale_data(X, Y, test_size=0.33, random_state=42)

    # Test 1: Check the shapes of the output arrays
    assert X_train.shape == (2, X.shape[1])
    assert X_test.shape == (1, X.shape[1])
    assert Y_train.shape == (2,)
    assert Y_test.shape == (1,)

    # Test 2: Check if the scaled training data has a mean close to 0
    assert np.all(np.isclose(X_train.mean(axis=0), 0))

    # Test 3: Check if the scaled training data has a standard deviation close to 1
    assert np.all(np.isclose(X_train.std(axis=0), 1))
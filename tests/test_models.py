import pytest
import numpy as np
from sklearn.linear_model import LogisticRegression
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.eval import evaluate_model

def test_evaluate_model():
    """A simple smoke test for the evaluate_model function."""
    # Create a dummy model
    model = LogisticRegression()

    # Create dummy data
    X_test = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y_test = np.array([0, 1, 0, 1])

    # Fit the model so it can predict
    model.fit(X_test, y_test)

    # Run the evaluation function
    metrics = evaluate_model(model, X_test, y_test)

    # Test 1: Check if the output is a dictionary
    assert isinstance(metrics, dict)

    # Test 2: Check if all expected metric keys are present
    expected_keys = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    assert all(key in metrics for key in expected_keys)

    # Test 3: Check that metric values are floats between 0 and 1
    for metric_name, value in metrics.items():
        assert isinstance(value, float)
        assert 0.0 <= value <= 1.0





import pytest
import yaml
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_config

@pytest.fixture
def create_test_config(tmp_path):
    """
    Creates a temporary YAML config file using pytest's tmp_path fixture.
    This is a robust way to test functions that read from files.
    """
    config_content = {
        'data_paths': {
            'raw': 'data/raw',
            'interim': 'data/interim'
        },
        'project_settings': {
            'target_column': 'class',
            'random_state': 42
        }
    }
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(config_content, f)
    return str(config_file)

def test_load_config(create_test_config):
    """Tests the load_config function."""
    config = load_config(create_test_config)

    # Test 1: Check if the output is a dictionary
    assert isinstance(config, dict)

    # Test 2: Check if the content is loaded correctly from the temp file
    assert config['data_paths']['raw'] == 'data/raw'
    assert config['project_settings']['target_column'] == 'class'
    assert config['project_settings']['random_state'] == 42
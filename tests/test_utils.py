import pytest
import yaml
import os
import sys

# Add the project root to the Python path to allow importing from `src`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_config

@pytest.fixture
def create_test_config(tmp_path):
    """
    Creates a temporary YAML config file using pytest's tmp_path fixture.
    This is a robust way to test functions that read from files without
    relying on the actual project files.
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
    # Create a file inside the temporary directory provided by pytest
    config_file = tmp_path / "test_config.yaml"
    
    # Write the sample dictionary to the yaml file
    with open(config_file, 'w') as f:
        yaml.dump(config_content, f)
        
    # Return the full path to the temporary file
    return str(config_file)

def test_load_config(create_test_config):
    """
    Tests the load_config function using the temporary config file
    created by the create_test_config fixture.
    """
    # Call the function we are testing
    config = load_config(create_test_config)

    # Test 1: Check if the output is a dictionary
    assert isinstance(config, dict)

    # Test 2: Check if the content was loaded correctly
    assert config['data_paths']['raw'] == 'data/raw'
    assert config['project_settings']['target_column'] == 'class'
    assert config['project_settings']['random_state'] == 42
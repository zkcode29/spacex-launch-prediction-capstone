import yaml
import joblib

def load_config(filepath='config/config.yaml'):
    """
    Loads a YAML configuration file.

    Args:
        filepath (str): The path to the configuration file.

    Returns:
        dict: A dictionary containing the configuration parameters.
    """
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def load_model(filepath):
    """
    Loads a model from a file using joblib.

    Args:
        filepath (str): The path to the model file.

    Returns:
        The loaded model object.
    """
    print(f"Loading model from {filepath}")
    return joblib.load(filepath)
#!/bin/bash

# This script launches the Plotly Dash dashboard.

echo "--- Starting the SpaceX Dashboard ---"

# Activate the virtual environment
source venv/bin/activate

# Run the dashboard application
# Using gunicorn for a more robust server than the default Dash server
# gunicorn app.dashboard:server --bind 0.0.0.0:8050

# Or, for development, run the python script directly
python3 app/dashboard.py

echo "--- Dashboard is running. Access it at http://127.0.0.1:8050 ---"
#!/bin/bash

# This script sets up the Python virtual environment for the project.

echo "--- Setting up Python virtual environment ---"

# Check if python3 is available
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found. Please install Python 3."
    exit
fi

# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

echo "--- Installing development dependencies ---"

# Upgrade pip
pip install --upgrade pip

# Install all required packages for development
pip install -r requirements/dev.txt

echo ""
echo "--- Environment setup complete! ---"
echo "To activate the environment, run: source venv/bin/activate"
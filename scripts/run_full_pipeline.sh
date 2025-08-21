#!/bin/bash

# This script runs the entire data science pipeline by executing the Python scripts in src/.

echo "--- Activating virtual environment ---"
source venv/bin/activate

echo "--- STEP 1: Running Data Collection ---"
python3 src/fetch_api.py
python3 src/scrape_wiki.py

# NOTE: For this project, the wrangling, training, and evaluation logic
# is orchestrated via notebooks. For a fully automated pipeline, you would
# create corresponding Python scripts (e.g., run_wrangling.py, run_training.py)
# and call them here.

echo "--- Full pipeline script finished ---"
echo "NOTE: Manual steps in Jupyter Notebooks are still required for this project."
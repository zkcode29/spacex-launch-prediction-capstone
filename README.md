

# SpaceX Falcon 9 First Stage Landing Prediction 

> A comprehensive, end-to-end data science capstone project that predicts the landing success of a SpaceX Falcon 9 first stage. This project covers the entire data science lifecycle, from data collection and cleaning to model training and the deployment of a fully interactive dashboard.

---

### Project Overview

The cost of a Falcon 9 launch is significantly reduced by SpaceX's ability to reuse the first stage. This project leverages public data to build a machine learning model that predicts landing outcomes, which can help in estimating the operational cost and risk of a launch.

#### Key Questions Answered:
- How do variables like payload mass, launch site, and orbit affect landing success?
- Has the rate of successful landings increased over the years?
- What is the best machine learning algorithm for this classification problem?

---

###  Project Structure

The repository is organized into a modular and reproducible structure, following best practices for data science projects.
```
spacex-landing-capstone/
├── app/ Plotly Dash application
├── config/ Configuration files (paths, parameters)
├── data/ Raw, interim, and processed data
├── docs/ Project documentation and reports
├── models/ Saved trained models
├── notebooks/ Jupyter notebooks for analysis (01 to 06)
├── requirements/ Python dependency files
├── scripts/ Automation shell scripts
├── src/ Reusable Python source code
├── sql/ SQL queries
└── tests/ Unit tests for the source code

```



### Tech Stack

This project utilizes a modern, industry-standard data science toolkit:

| Category              | Technologies Used                                    |
| --------------------- | ---------------------------------------------------- |
| **Core Language**     | `Python`                                             |
| **Data Manipulation** | `Pandas`, `NumPy`                                    |
| **Data Collection**   | `Requests`, `BeautifulSoup4`                         |
| **Machine Learning**  | `Scikit-learn`                                       |
| **Data Visualization**| `Matplotlib`, `Seaborn`, `Plotly`                    |
| **Dashboarding**      | `Plotly Dash`, `Dash Bootstrap Components`           |
| **Geospatial Analysis**| `Folium`                                            |
| **Testing**           | `Pytest`                                             |

---


 ## Getting Started & Running the Project

Follow these steps to get the project running on your local machine.

## Step 1: Clone the Repository

First, clone the project to your computer using Git.
```
git clone https://github.com/zkcode29/spacex-launch-prediction-capstone.git
cd spacex-landing-capstone
```
## Step 2: Set Up the Environment & Install Dependencies

This project uses a virtual environment to manage its libraries. Choose the instructions for your operating system.

**On Windows (using PowerShell):**
```
# 1. Create the virtual environment
python -m venv venv

# 2. Allow activation scripts to run for this session
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 3. Activate the environment
.\venv\Scripts\Activate.ps1

# 4. Install all required libraries
pip install -r requirements/dev.txt
```


**On macOS / Linux (using Terminal):**
```
# The Makefile automates this entire process
make setup

# If you don't use make, you must activate the environment manually
source venv/bin/activate
```
## Step 3: Run the Data Collection Pipeline
Next, run the scripts that fetch the raw data from the internet.

**On Windows (using PowerShell):**
```
python src/fetch_api.py
python src/scrape_wiki.py
```
**On macOS / Linux (using Terminal):**
```
make data
```
This will populate the data/raw/ directory with the necessary files.
## Step 4: Execute the Jupyter Notebooks

The core analysis and model training is done in Jupyter Notebooks.
1.  Open the `notebooks/` directory in your code editor (like VS Code).
2.  Run the notebooks in sequential order, from `01_data_collection.ipynb` to `06_final_analysis.ipynb`.
3.  This will clean the data, perform the analysis, train the models, and save the best one.

## Step 5: Launch the Interactive Dashboard

Finally, launch the web application to see the results.

**On Windows (using PowerShell):**
```
python app/dashboard.py
```
**On macOS / Linux (using Terminal):**
```
make app
```
After running the command, open your web browser and navigate to the following address to view your live dashboard:

http://127.0.0.1:8050

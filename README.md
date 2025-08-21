# SpaceX Falcon 9 First Stage Landing Prediction

This is a comprehensive data science capstone project that aims to predict whether the first stage of a SpaceX Falcon 9 rocket will land successfully. The project encompasses the entire data science lifecycle, from data collection and cleaning to model training and deployment of an interactive dashboard.

## 🚀 Project Overview

The cost of a Falcon 9 launch is significantly reduced by SpaceX's ability to reuse the first stage. This model uses public data to predict landing outcomes, which can help in estimating the operational cost of a launch.

### Key Questions
- How do variables like payload mass, launch site, and orbit affect landing success?
- Has the rate of successful landings increased over the years?
- What is the best machine learning algorithm for this classification problem?

## 📂 Project Structure
The project is organized into a modular and reproducible structure:

spacex-landing-capstone/
├── app/ # Plotly Dash application
├── config/ # Configuration files (paths, parameters)
├── data/ # Raw, interim, and processed data
├── docs/ # Project documentation and reports
├── models/ # Saved trained models
├── notebooks/ # Jupyter notebooks for analysis (01 to 06)
├── requirements/ # Python dependency files
├── scripts/ # Automation shell scripts
├── src/ # Reusable Python source code
├── sql/ # SQL queries
└── tests/ # Unit tests for the source code


## 🛠️ Tech Stack
- **Python**
- **Data Manipulation:** Pandas, NumPy
- **Data Collection:** Requests, BeautifulSoup4
- **Machine Learning:** Scikit-learn
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Dashboarding:** Plotly Dash
- **Geospatial Analysis:** Folium
- **Testing:** Pytest

## 🏁 Getting Started

### Prerequisites
- Python 3.8 or higher
- A virtual environment tool (like `venv`)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/[your-username]/spacex-landing-capstone.git
    cd spacex-landing-capstone
    ```

2.  **Set up the environment and install dependencies using the Makefile:**
    ```bash
    make setup
    ```
    This will create a `venv` folder and install all necessary packages.

3.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```

### Running the Pipeline

1.  **Collect the data:**
    Run the data collection scripts.
    ```bash
    make data
    ```
    This populates the `data/raw/` directory.

2.  **Execute the Jupyter Notebooks:**
    Open the `notebooks/` directory and run the notebooks in sequential order, from `01_data_collection.ipynb` to `06_final_analysis.ipynb`.

### Launching the Dashboard
To view the interactive dashboard, run:
```bash
make app



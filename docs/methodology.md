# Data Science Methodology

This project followed a structured data science lifecycle, outlined below.

### 1. Data Collection
- **Source 1: SpaceX API:** Utilized the `requests` library in Python to programmatically fetch all historical launch data from the `v4/launches` endpoint. The nested JSON response was flattened into a tabular format using `pandas.json_normalize`.
- **Source 2: Wikipedia:** Scraped HTML tables from the "List of Falcon 9 and Falcon Heavy launches" page using `pandas.read_html`.

### 2. Data Wrangling & Cleaning
- Merged the API and scraped Wikipedia data.
- Handled missing values through various strategies (e.g., imputation, removal).
- Standardized column names and data types.
- Extracted key information from nested or text-based columns (e.g., Orbit type, Launch Site).
- Created the binary target variable `class` (1 for successful landing, 0 for failure).

### 3. Exploratory Data Analysis (EDA)
- Utilized SQL queries to aggregate and summarize the data.
- Generated visualizations using Matplotlib, Seaborn, and Plotly to understand relationships between variables.
- Analyzed trends, such as the increase in landing success rates over time.
- Created interactive geographical maps of launch sites using Folium.

### 4. Feature Engineering
- Applied One-Hot Encoding to convert categorical features (e.g., `LaunchSite`, `Orbit`) into a numerical format suitable for machine learning models.
- Scaled numerical features like `PayloadMass` and `FlightNumber` using `StandardScaler` to prevent model bias.
- Split the dataset into training and testing sets (80/20 split).

### 5. Predictive Modeling
- Trained several binary classification models:
  - Logistic Regression
  - Support Vector Machine (SVM)
  - Decision Tree
  - Random Forest
- Employed GridSearchCV to systematically tune hyperparameters for each model to find the optimal settings.

### 6. Model Evaluation
- Evaluated each model on the held-out test set using the following metrics:
  - **Accuracy:** Overall correctness.
  - **Precision:** Ability to avoid false positives.
  - **Recall:** Ability to find all true positives.
  - **F1-Score:** The harmonic mean of Precision and Recall.
- The best-performing model was selected based on a holistic review of these metrics.
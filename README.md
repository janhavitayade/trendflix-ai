# 🎬 TrendFlix AI

TrendFlix AI is an OTT Trend Intelligence Platform that collects live TV show data, stores historical snapshots, performs SQL analytics, trains machine learning models, and visualizes insights through an interactive Streamlit dashboard.

🔗 **Live app:** [trendflix-ai.streamlit.app](https://trendflix-ai.streamlit.app/)

## Project Objective

The goal of TrendFlix AI is to analyze OTT content trends and forecast future popularity patterns. The platform combines data collection, database management, analytics, machine learning, and visualization into a complete end-to-end data science project.

---
## Quick Start

### Clone Repository

```bash
git clone https://github.com/janhavitayade/trendflix-ai.git
cd trendflix-ai
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Generate the Production Model

Before running the dashboard, generate the trained model artifacts used by the Predict page:

```bash
python src/ml/benchmark_models.py
```

This prints the model leaderboard and saves two files to `models/`:

* `extra_trees_model.pkl` — the trained production model (Extra Trees Regressor)
* `feature_columns.pkl` — the exact feature order the model expects

Re-run this any time `data/ml_dataset.csv` or the model logic changes.

### Run Dashboard

```bash
streamlit run app/app.py
```


## Current Features

### 📡 Data Collection

* Fetches live TV show data from the TVMaze API
* Stores raw API responses as CSV snapshots
* Maintains historical records for trend analysis

### 🗄 Database Management

* SQLite database integration
* Structured storage of TV show metadata
* Historical snapshot tracking with timestamps
* Dedicated tables for analytics and machine learning

### 📊 Analytics Layer

* SQL-based analytics and reporting
* Top-rated show analysis
* Language distribution analysis
* Show status distribution analysis
* Popularity (weight) analysis
* Missing value detection and data quality checks

### 🤖 Machine Learning

* Machine learning dataset generation
* Feature engineering and preprocessing
* Multiple model benchmarking
* Production-ready model selection
* Model persistence with `joblib` for live inference
* Feature importance analysis
* Model evaluation using:

  * MAE (Mean Absolute Error)
  * MSE (Mean Squared Error)
  * R² Score

### 🔮 Live Prediction

* Interactive "Predict" page in the dashboard
* Users enter unseen/hypothetical show attributes (rating, status, premiere year, runtime, genre count)
* `show_age` is auto-calculated from premiere year
* Returns a live popularity (`weight`) prediction from the saved Extra Trees Regressor — no retraining required at runtime

### 📈 Dashboard

* Interactive Streamlit dashboard
* KPI cards for platform statistics
* Top-rated shows table
* Status distribution visualization
* Language distribution visualization
* Model leaderboard
* Feature importance visualization
* Live prediction interface
* Dataset explorer

---

## Tech Stack

* Python
* TVMaze API
* SQLite
* Pandas
* SQL
* Scikit-Learn
* Joblib
* Streamlit
* Git & GitHub

---

## Project Structure

```text
OTT-Trend-Intelligence/
│
│                       
├───app
│       app.py
│       
├───assets
│       trendflix_favicon.png
│       trendflix_logo.png
│       trendflix_logo.svg
│       
├───data
│       ml_dataset.csv
│       tvmaze_shows_20260712_132104.csv
│       
├───database
│       trendflix.db
│       
├───models
│       extra_trees_model.pkl
│       feature_columns.pkl
│       
├───notebooks
└───src
    │   fetch_tvmaze.py
    │   __init__.py
    │   
    ├───database
    │       analytics_queries.py
    │       create_database.py
    │       create_everything_table.py
    │       insert_everything_into_table_everything.py
    │       insert_shows.py
    │       insert_snapshots.py
    │       query_shows.py
    │       
    └───ml
        │   benchmark_models.py
        │   feature_importance.py
        │   final_model.py
        │   prepare_dataset_v2.py
        │   
        └───archive
                prepare_dataset_v1.py
                train_model_v1.py
                train_model_v2.py
                train_random_forest.py
                tvmaze_shows_20260708_135132.csv
```

---

## Data Flow

```text
TVMaze API
      ↓
fetch_tvmaze.py
      ↓
CSV Snapshot
      ↓
SQLite Database
      ↓
shows / snapshots / everything
      ↓
SQL Analytics
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Model Benchmarking
      ↓
Feature Importance
      ↓
Model Persistence (joblib)
      ↓
Streamlit Dashboard (Live Prediction)
```

---

## Database Design

### shows

Stores relatively static information about TV shows.

Fields:

* id
* name
* language
* status
* premiered
* ended
* weight

---

### snapshots

Stores historical observations for trend analysis.

Fields:

* snapshot_id
* show_id
* weight
* rating
* collected_at

---

### everything

Stores detailed TVMaze metadata for advanced analytics and machine learning.

Includes:

* id
* name
* type
* language
* genres
* status
* runtime
* averageRuntime
* premiered
* ended
* rating
* weight
* network
* summary
* updated
* and other TVMaze attributes

---

## Project Results

### Dataset Statistics

* Total TV Shows: 240
* Historical Snapshots: 240
* Features Engineered: 6
* Machine Learning Models Compared: 5

---

### Model Leaderboard

| Model             |  MAE |    MSE |   R² |
| ----------------- | ---: | -----: | ---: |
| Extra Trees       | 6.40 | 148.68 | 0.26 |
| Random Forest     | 6.57 | 150.97 | 0.25 |
| Decision Tree     | 7.18 | 160.23 | 0.21 |
| Gradient Boosting | 6.79 | 167.24 | 0.17 |
| Linear Regression | 7.32 | 178.16 | 0.12 |

---

### Production Model

**Extra Trees Regressor**

Performance:

```text
MAE: 6.40
MSE: 148.68
R² Score: 0.26
```

The Extra Trees Regressor achieved the highest predictive performance and was selected as the final production model for TrendFlix AI. It is persisted with `joblib` (`models/extra_trees_model.pkl`) and loaded directly by the Streamlit dashboard's Predict page for live inference, with no retraining at request time.

> **Note:** the Predict page's `status_encoded` mapping assumes alphabetical label encoding (`Ended = 0, Running = 1, To Be Determined = 2`), matching scikit-learn's default `LabelEncoder` behavior. If the original preprocessing pipeline used a different mapping, update `STATUS_ENCODING_MAP` in `app/app.py` to match.

---

### Feature Importance

| Feature        | Importance (%) |
| -------------- | -------------: |
| rating         |          52.58 |
| averageRuntime |          14.88 |
| premiered_year |          10.65 |
| show_age       |          10.24 |
| genre_count    |           8.44 |
| status_encoded |           3.21 |

Key insight: TV show ratings are by far the strongest predictor of popularity weight in the current dataset.

---

## Machine Learning Pipeline

### Dataset V1

Features:

* rating
* status_encoded
* premiered_year

Performance:

```text
MAE: 7.04
MSE: 154.07
R² Score: 0.13
```

---

### Dataset V2 (updated over V1)

Additional engineered features:

* averageRuntime
* genre_count
* show_age

Used for benchmarking multiple machine learning algorithms and feature importance analysis.

---

### Model Persistence & Live Inference

The production model (Extra Trees Regressor) and its expected feature column order are saved with `joblib` after benchmarking:

* `models/extra_trees_model.pkl`
* `models/feature_columns.pkl`

The Streamlit dashboard loads both artifacts once (cached with `st.cache_resource`) and uses them to score user-entered inputs on the Predict page, without needing scikit-learn to retrain anything at runtime.

---

## Dashboard Features

### Overview

* Platform statistics
* Project architecture
* KPI metrics

### Analytics

* Top-rated shows
* Status distribution
* Language distribution
* Show filtering

### Machine Learning

* Production model summary
* Model leaderboard
* Feature importance chart

### Predict

* Live popularity prediction from user-entered show attributes
* Powered by the saved Extra Trees Regressor
* Auto-calculated `show_age` from premiere year

### Dataset Explorer

* Search TV shows
* Interactive dataset browsing

---

## Progress

### ✅ Completed

* TVMaze API Integration
* CSV Data Storage
* SQLite Database Setup
* Historical Snapshot Tracking
* SQL Analytics & Reporting
* Data Cleaning & Preprocessing
* Machine Learning Dataset Creation
* Feature Engineering
* Model Benchmarking
* Feature Importance Analysis
* Production Model Selection
* Model Persistence (joblib)
* Live Prediction Interface
* Streamlit Dashboard
* GitHub Version Control
* Deployment to Streamlit Community Cloud

### 📌 Planned

* Automated Data Refresh Pipeline
* Advanced Forecasting Models

---

## Future Vision

TrendFlix AI aims to become a complete OTT trend intelligence platform capable of collecting live entertainment data, analyzing historical patterns, forecasting popularity trends, benchmarking machine learning models, and presenting insights through an interactive AI-powered dashboard.

---

## Author

**Janhavi Tayade**
# 🎬 TrendFlix AI

TrendFlix AI is an OTT Trend Intelligence Platform that collects live TV show data, stores historical snapshots, performs SQL analytics, trains machine learning models, and visualizes insights through an interactive Streamlit dashboard.

## Project Objective

The goal of TrendFlix AI is to analyze OTT content trends and forecast future popularity patterns. The platform combines data collection, database management, analytics, machine learning, and visualization into a complete end-to-end data science project.

---

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
* Linear Regression model training
* Model evaluation using:

  * MAE (Mean Absolute Error)
  * MSE (Mean Squared Error)
  * R² Score
* Feature engineering experiments and model comparison

### 📈 Dashboard

* Interactive Streamlit dashboard
* KPI cards for platform statistics
* Top-rated shows table
* Status distribution visualization
* Language distribution visualization
* Machine learning model summary
* Dataset preview

---

## Tech Stack

* Python
* TVMaze API
* SQLite
* Pandas
* SQL
* Scikit-Learn
* Streamlit
* Git & GitHub

---

## Project Structure

```text
TrendFlix-AI/
│
├───app
│       
├───data
│       ml_dataset.csv
│       tvmaze_shows_20260708_135132.csv
│       
├───database
│       trendflix.db
│       
├───models
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
            prepare_dataset_v1.py
            prepare_dataset_v2.py
            train_model_v1.py
            train_model_v2.py
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
Machine Learning
      ↓
Streamlit Dashboard
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

## Machine Learning Pipeline

### Dataset V1

Features:

* rating
* status_encoded
* premiered_year

Target:

* weight

Performance:

```text
MAE: 7.04
MSE: 154.07
R² Score: 0.13
```

---

### Dataset V2 (Feature Engineering Experiment)

Additional Features:

* averageRuntime
* genre_count
* show_age

Performance:

```text
MAE: 7.32
MSE: 178.16
R² Score: 0.12
```

Conclusion:

Feature engineering experiment completed and evaluated. Additional engineered features did not improve model performance, highlighting the importance of feature quality over feature quantity.

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
* Linear Regression Model Training
* Feature Engineering Experiments
* Streamlit Dashboard V1
* GitHub Version Control

### 🚧 In Progress

* Dashboard Enhancements
* Machine Learning Improvements

### 📌 Planned

* Random Forest Model
* Gradient Boosting Model
* Model Comparison Dashboard
* Trend Forecasting Improvements
* Deployment

---

## Future Vision

TrendFlix AI aims to become a complete OTT trend intelligence platform capable of collecting live entertainment data, analyzing historical patterns, forecasting popularity trends, and presenting insights through an interactive AI-powered dashboard.

---

## Author

**Janhavi Tayade**

# TrendFlix AI

TrendFlix AI is an OTT Trend Intelligence Platform that collects live TV show data, stores historical snapshots, performs analytics, and aims to forecast future content popularity using Machine Learning.

## Project Objective

The goal of TrendFlix AI is to analyze OTT content trends and predict future popularity patterns. The platform collects data from public APIs, stores historical records, generates analytical insights, and will eventually provide AI-powered trend forecasting through an interactive dashboard.

---

## Current Features

### Data Collection

* Fetches live TV show data from the TVMaze API
* Stores raw data as CSV snapshots
* Maintains historical records for analysis

### Database Management

* SQLite database integration
* Structured storage of TV show metadata
* Historical snapshot tracking with timestamps

### Analytics Layer

* SQL-based analytics and reporting
* Top-rated show analysis
* Language distribution analysis
* Show status distribution analysis
* Popularity (weight) analysis
* Data quality checks for missing values

---

## Tech Stack

* Python
* TVMaze API
* SQLite
* Pandas
* SQL
* Git & GitHub
* Scikit-Learn (Planned)
* Streamlit (Planned)

---

## Project Structure

```text
TrendFlix-AI/
│
├── app/                  # Streamlit dashboard (future)
├── data/                 # Raw CSV snapshots
├── database/             # SQLite database
│   └── trendflix.db
├── models/               # ML models (future)
├── notebooks/            # Experiments and analysis
├── src/
│   ├── fetch_tvmaze.py
│   ├── __init__.py
│   └── database/
│       ├── create_database.py
│       ├── insert_shows.py
│       ├── insert_snapshots.py
│       ├── query_shows.py
│       └── analytics_queries.py
│
├── requirements.txt
├── README.md
└── .gitignore
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
insert_shows.py
      ↓
shows table
      ↓
insert_snapshots.py
      ↓
snapshots table
      ↓
analytics_queries.py
      ↓
Insights & Reports
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

### snapshots

Stores historical observations for trend analysis.

Fields:

* snapshot_id
* show_id
* weight
* rating
* collected_at

---

## Progress

### Completed

* API Integration
* CSV Data Storage
* SQLite Database Setup
* Historical Snapshot Tracking
* SQL Analytics & Reporting
* GitHub Version Control

### In Progress

* Data Preparation for Machine Learning

### Planned

* Trend Forecasting Model
* Streamlit Dashboard
* Interactive Visualizations
* Deployment

---

## Future Vision

TrendFlix AI will forecast OTT content popularity by analyzing historical trends and presenting insights through an interactive dashboard. The final system will combine data engineering, analytics, machine learning, and visualization into a single end-to-end project.

## Author

Janhavi Tayade

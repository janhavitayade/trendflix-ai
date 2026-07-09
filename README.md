# TrendFlix AI

TrendFlix AI is an OTT Trend Intelligence Platform that collects live TV show data from the TVMaze API, stores it in a SQLite database, tracks popularity trends over time, and will eventually use machine learning to forecast future entertainment trends.

## Project Goal

Build an end-to-end data platform that:

* Collects live OTT-related data from public APIs
* Stores and manages data using SQLite
* Tracks historical popularity snapshots
* Performs trend analysis and visualization
* Predicts future content trends using Machine Learning
* Presents insights through an interactive dashboard

## Current Architecture

TVMaze API → Python → SQLite Database → SQL Analytics

## Tech Stack

### Data Collection

* Python
* Requests
* TVMaze API

### Data Storage

* SQLite

### Data Processing

* Pandas

### Machine Learning (Planned)

* Scikit-Learn

### Visualization & Dashboard (Planned)

* Streamlit

### Version Control

* Git
* GitHub

## Project Structure

```text
OTT-Trend-Intelligence
│
├── app/
├── data/
├── database/
├── models/
├── notebooks/
├── src/
│   ├── fetch_tvmaze.py
│   └── database/
│       ├── create_database.py
│       ├── insert_shows.py
│       └── query_shows.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Progress

### Day 1

* Connected to TVMaze API
* Fetched live TV show data
* Stored data in CSV format
* Set up Git and GitHub repository

### Day 2

* Created SQLite database
* Created `shows` table
* Inserted 240 live records
* Executed SQL analytics queries
* Established the first version of the data pipeline

## Current Status

✅ Live API Integration Complete

✅ SQLite Database Integration Complete

✅ SQL Querying Complete

🚧 Historical Trend Tracking (Next Phase)

🚧 Machine Learning Pipeline (Planned)

🚧 Interactive Dashboard (Planned)

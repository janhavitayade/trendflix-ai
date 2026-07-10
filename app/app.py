import streamlit as st
import sqlite3
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="TrendFlix AI",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

connection = sqlite3.connect("database/trendflix.db")

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎬 TrendFlix AI")
st.subheader("OTT Trend Intelligence Platform")

st.markdown(
    """
    Collecting live TV show data from the TVMaze API,
    performing analytics using SQL, and applying machine
    learning to forecast content popularity trends.
    """
)

st.divider()

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------

shows_query = """
SELECT *
FROM shows
"""

shows_df = pd.read_sql_query(shows_query, connection)

total_shows = len(shows_df)

running_shows = len(
    shows_df[shows_df["status"] == "Running"]
)

ended_shows = len(
    shows_df[shows_df["status"] == "Ended"]
)

avg_rating_query = """
SELECT AVG(rating)
FROM snapshots
WHERE rating IS NOT NULL
"""

avg_rating = pd.read_sql_query(
    avg_rating_query,
    connection
).iloc[0, 0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Shows",
        total_shows
    )

with col2:
    st.metric(
        "Running Shows",
        running_shows
    )

with col3:
    st.metric(
        "Ended Shows",
        ended_shows
    )

with col4:
    st.metric(
        "Average Rating",
        round(avg_rating, 2)
    )

st.divider()

# --------------------------------------------------
# TOP RATED SHOWS
# --------------------------------------------------

st.subheader("⭐ Top 10 Highest Rated Shows")

top_rated_query = """
SELECT
    shows.name,
    snapshots.rating
FROM shows
JOIN snapshots
ON shows.id = snapshots.show_id
WHERE snapshots.rating IS NOT NULL
ORDER BY snapshots.rating DESC
LIMIT 10
"""

top_rated_df = pd.read_sql_query(
    top_rated_query,
    connection
)

st.dataframe(
    top_rated_df,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# STATUS DISTRIBUTION
# --------------------------------------------------

st.subheader("📺 Show Status Distribution")

status_query = """
SELECT
    status,
    COUNT(*) AS count
FROM shows
GROUP BY status
"""

status_df = pd.read_sql_query(
    status_query,
    connection
)

st.bar_chart(
    status_df.set_index("status")
)

st.divider()

# --------------------------------------------------
# LANGUAGE DISTRIBUTION
# --------------------------------------------------

st.subheader("🌍 Language Distribution")

language_query = """
SELECT
    language,
    COUNT(*) AS count
FROM shows
GROUP BY language
ORDER BY count DESC
"""

language_df = pd.read_sql_query(
    language_query,
    connection
)

st.bar_chart(
    language_df.set_index("language")
)

st.divider()

# --------------------------------------------------
# MACHINE LEARNING SECTION
# --------------------------------------------------

st.subheader("🤖 Machine Learning Model")

st.info(
    """
    Current Model: Linear Regression

    Features Used:
    • rating
    • status_encoded
    • premiered_year

    Model Performance:
    • MAE = 7.04
    • MSE = 154.07
    • R² Score = 0.13
    """
)

st.divider()

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

st.subheader("🗂 Dataset Preview")

st.dataframe(
    shows_df.head(),
    use_container_width=True
)

# --------------------------------------------------
# CLOSE CONNECTION
# --------------------------------------------------

connection.close()

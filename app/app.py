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
# LOAD DATA
# --------------------------------------------------

shows_query = """
SELECT *
FROM shows
"""

shows_df = pd.read_sql_query(
    shows_query,
    connection
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

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_shows = len(shows_df)

running_shows = len(
    shows_df[
        shows_df["status"] == "Running"
    ]
)

ended_shows = len(
    shows_df[
        shows_df["status"] == "Ended"
    ]
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎬 TrendFlix AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Analytics",
        "Machine Learning",
        "Dataset Explorer"
    ]
)

# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------

if page == "Overview":

    st.title("🎬 TrendFlix AI")
    st.subheader("OTT Trend Intelligence Platform")

    st.markdown(
        """
        TrendFlix AI collects live TV show data from the TVMaze API,
        stores historical records in SQLite, performs SQL analytics,
        and applies machine learning to forecast content popularity.
        """
    )

    st.divider()

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

    st.subheader("Project Architecture")

    st.code(
        """
TVMaze API
      ↓
CSV Snapshots
      ↓
SQLite Database
      ↓
SQL Analytics
      ↓
Machine Learning
      ↓
Streamlit Dashboard
        """
    )

# --------------------------------------------------
# ANALYTICS PAGE
# --------------------------------------------------

elif page == "Analytics":

    st.title("📊 Analytics Dashboard")

    status_filter = st.selectbox(
        "Filter by Status",
        [
            "All",
            "Running",
            "Ended",
            "To Be Determined"
        ]
    )

    if status_filter == "All":
        filtered_df = shows_df
    else:
        filtered_df = shows_df[
            shows_df["status"] == status_filter
        ]

    st.subheader("Filtered Shows")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.divider()

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

# --------------------------------------------------
# MACHINE LEARNING PAGE
# --------------------------------------------------

elif page == "Machine Learning":

    st.title("🤖 Machine Learning")

    st.subheader("Best Model")

    st.success("Random Forest Regressor")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "MAE",
            "6.57"
        )

    with col2:
        st.metric(
            "MSE",
            "150.97"
        )

    with col3:
        st.metric(
            "R² Score",
            "0.25"
        )

    st.divider()

    st.subheader("Features Used")

    st.write("• rating")
    st.write("• status_encoded")
    st.write("• premiered_year")
    st.write("• averageRuntime")
    st.write("• genre_count")
    st.write("• show_age")

    st.divider()

    st.subheader("Model Comparison")

    comparison_df = pd.DataFrame(
        {
            "Model": [
                "Linear Regression",
                "Random Forest"
            ],
            "MAE": [
                7.32,
                6.57
            ],
            "MSE": [
                178.16,
                150.97
            ],
            "R²": [
                0.12,
                0.25
            ]
        }
    )

    st.dataframe(
        comparison_df,
        use_container_width=True
    )

    st.divider()

    st.info(
        """
        Random Forest Regressor achieved the best performance
        among the tested models and is currently the primary
        forecasting model used in TrendFlix AI.
        """
    )

# --------------------------------------------------
# DATASET EXPLORER PAGE
# --------------------------------------------------

elif page == "Dataset Explorer":

    st.title("🗂 Dataset Explorer")

    search = st.text_input(
        "Search Show Name"
    )

    if search:

        filtered_df = shows_df[
            shows_df["name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    else:
        filtered_df = shows_df

    st.write(
        f"Rows Found: {len(filtered_df)}"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# --------------------------------------------------
# CLOSE CONNECTION
# --------------------------------------------------

connection.close()

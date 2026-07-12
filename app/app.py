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

shows_df = pd.read_sql_query(
    "SELECT * FROM shows",
    connection
)

avg_rating = pd.read_sql_query(
    """
    SELECT AVG(rating)
    FROM snapshots
    WHERE rating IS NOT NULL
    """,
    connection
).iloc[0, 0]

snapshot_count = pd.read_sql_query(
    """
    SELECT COUNT(*) AS total
    FROM snapshots
    """,
    connection
).iloc[0, 0]

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_shows = len(shows_df)

running_shows = len(
    shows_df[shows_df["status"] == "Running"]
)

ended_shows = len(
    shows_df[shows_df["status"] == "Ended"]
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
        st.metric("Total Shows", total_shows)

    with col2:
        st.metric("Running Shows", running_shows)

    with col3:
        st.metric("Ended Shows", ended_shows)

    with col4:
        st.metric(
            "Average Rating",
            round(avg_rating, 2)
        )

    st.divider()

    st.subheader("Project Summary")

    st.info(
        f"""
        Data Source: TVMaze API

        Database: SQLite

        Shows: {total_shows}

        Snapshots: {snapshot_count}

        Best Model: Extra Trees Regressor

        R² Score: 0.26
        """
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

    top_rated_df = pd.read_sql_query(
        """
        SELECT
            shows.name,
            snapshots.rating
        FROM shows
        JOIN snapshots
        ON shows.id = snapshots.show_id
        WHERE snapshots.rating IS NOT NULL
        ORDER BY snapshots.rating DESC
        LIMIT 10
        """,
        connection
    )

    st.dataframe(
        top_rated_df,
        use_container_width=True
    )

    st.divider()

    st.subheader("📺 Show Status Distribution")

    status_df = pd.read_sql_query(
        """
        SELECT
            status,
            COUNT(*) AS count
        FROM shows
        GROUP BY status
        """,
        connection
    )

    st.bar_chart(
        status_df.set_index("status")
    )

    st.divider()

    st.subheader("🌍 Language Distribution")

    language_df = pd.read_sql_query(
        """
        SELECT
            language,
            COUNT(*) AS count
        FROM shows
        GROUP BY language
        ORDER BY count DESC
        """,
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

    st.success("🏆 Extra Trees Regressor")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("MAE", "6.40")

    with col2:
        st.metric("MSE", "148.68")

    with col3:
        st.metric("R² Score", "0.26")

    st.divider()

    st.subheader("Features Used")

    st.write("• rating")
    st.write("• status_encoded")
    st.write("• premiered_year")
    st.write("• averageRuntime")
    st.write("• genre_count")
    st.write("• show_age")

    st.divider()

    st.subheader("Model Leaderboard")

    comparison_df = pd.DataFrame(
        {
            "Model": [
                "Extra Trees",
                "Random Forest",
                "Decision Tree",
                "Gradient Boosting",
                "Linear Regression"
            ],
            "MAE": [
                6.40,
                6.57,
                7.18,
                6.79,
                7.32
            ],
            "MSE": [
                148.68,
                150.97,
                160.23,
                167.24,
                178.16
            ],
            "R²": [
                0.26,
                0.25,
                0.21,
                0.17,
                0.12
            ]
        }
    )

    st.dataframe(
        comparison_df,
        use_container_width=True
    )

    st.divider()

    st.subheader("Feature Importance")

    importance_df = pd.DataFrame(
        {
            "Feature": [
                "rating",
                "averageRuntime",
                "premiered_year",
                "show_age",
                "genre_count",
                "status_encoded"
            ],
            "Importance": [
                52.5777,
                14.8818,
                10.6499,
                10.2377,
                8.4437,
                3.2093
            ]
        }
    )

    st.bar_chart(
        importance_df.set_index("Feature")
    )

    st.info(
        """
        Key Insight:

        Rating is the strongest predictor of popularity,
        contributing over 52% of the model's decision-making.

        Runtime, show age, and premiere year also influence
        popularity, while show status has minimal impact.
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

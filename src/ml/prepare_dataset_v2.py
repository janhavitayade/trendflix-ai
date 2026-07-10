import sqlite3
import pandas as pd
import json

# Connect to database
connection = sqlite3.connect("database/trendflix.db")

# Read from everything table
query = """
SELECT
    rating,
    status,
    premiered,
    averageRuntime,
    genres,
    weight
FROM everything
"""

df = pd.read_sql_query(query, connection)

connection.close()

# Remove rows with missing ratings
df = df.dropna(subset=["rating"])

# Create premiered_year
df["premiered_year"] = pd.to_datetime(df["premiered"]).dt.year

# Create show_age
CURRENT_YEAR = 2026

df["show_age"] = CURRENT_YEAR - df["premiered_year"]

# Encode status
status_mapping = {
    "Ended": 0,
    "Running": 1,
    "To Be Determined": 2
}

df["status_encoded"] = df["status"].map(status_mapping)

# Create genre_count
def count_genres(genres_string):

    genres_list = json.loads(genres_string)

    return len(genres_list)

df["genre_count"] = df["genres"].apply(count_genres)

# Keep only ML columns
df = df[
    [
        "rating",
        "status_encoded",
        "premiered_year",
        "averageRuntime",
        "genre_count",
        "show_age",
        "weight"
    ]
]

# Save dataset
df.to_csv("data/ml_dataset.csv", index=False)

print("ML Dataset V2 created successfully!")

print("\nFirst 5 Rows:\n")

print(df.head())
import sqlite3
import pandas as pd

# Connect to database
connection = sqlite3.connect("database/trendflix.db")

# Join shows and snapshots tables
query = """
SELECT
    snapshots.rating,
    shows.status,
    shows.premiered,
    shows.weight
FROM shows
JOIN snapshots
ON shows.id = snapshots.show_id
"""

df = pd.read_sql_query(query, connection)

connection.close()

# Remove rows with missing ratings
df = df.dropna(subset=["rating"])

# Create premiered_year feature
df["premiered_year"] = pd.to_datetime(df["premiered"]).dt.year

# Encode status
status_mapping = {
    "Ended": 0,
    "Running": 1,
    "To Be Determined": 2
}

df["status_encoded"] = df["status"].map(status_mapping)

# Keep only ML columns
df = df[
    [
        "rating",
        "status_encoded",
        "premiered_year",
        "weight"
    ]
]

# Save dataset
df.to_csv("data/ml_dataset.csv", index=False)

print("ML dataset created successfully!")
print("\nFirst 5 Rows:\n")
print(df.head())
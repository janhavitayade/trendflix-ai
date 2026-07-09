import requests
import sqlite3
from datetime import datetime

url = "https://api.tvmaze.com/shows"

response = requests.get(url)

if response.status_code == 200:

    shows = response.json()

    connection = sqlite3.connect("database/trendflix.db")
    cursor = connection.cursor()

    inserted_count = 0

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for show in shows:

        rating = show.get("rating", {}).get("average")

        cursor.execute("""
        INSERT INTO snapshots
        (
            show_id,
            weight,
            rating,
            collected_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            show.get("id"),
            show.get("weight"),
            rating,
            timestamp
        ))

        inserted_count += 1

    connection.commit()
    connection.close()

    print(f"{inserted_count} snapshots inserted successfully!")

else:
    print("Failed to fetch data")
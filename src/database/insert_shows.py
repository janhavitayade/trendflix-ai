# This script fetches data from the TVMaze API and inserts it into the 'shows' table in the 'trendflix.db' SQLite database.
# It uses the 'INSERT OR REPLACE' statement to avoid duplicate primary-key errors by updating existing records if they already exist.

import requests
import sqlite3

url = "https://api.tvmaze.com/shows"

response = requests.get(url) #gets the live TVMaze data

if response.status_code == 200:

    shows = response.json()

    connection = sqlite3.connect("database/trendflix.db") # connects to trendflix.db
    cursor = connection.cursor()

    inserted_count = 0

    for show in shows:

# If row doesn't exist → insert
#f row already exists → update
#This prevents duplicate primary-key errors.
        cursor.execute("""
        INSERT OR REPLACE INTO shows
        (
            id,
            name,
            language,
            status,
            premiered,
            ended,
            weight
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            show.get("id"),
            show.get("name"),
            show.get("language"),
            show.get("status"),
            show.get("premiered"),
            show.get("ended"),
            show.get("weight")
        ))

        inserted_count += 1

    connection.commit()
    connection.close()

    print(f"{inserted_count} records inserted successfully!")

else:
    print("Failed to fetch data")
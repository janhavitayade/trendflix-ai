import requests
import sqlite3
import json

url = "https://api.tvmaze.com/shows"

response = requests.get(url)

if response.status_code == 200:

    shows = response.json()

    connection = sqlite3.connect("database/trendflix.db")
    cursor = connection.cursor()

    inserted_count = 0

    for show in shows:

        cursor.execute("""
        INSERT OR REPLACE INTO everything
        (
            id,
            url,
            name,
            type,
            language,
            genres,
            status,
            runtime,
            averageRuntime,
            premiered,
            ended,
            officialSite,
            schedule,
            rating,
            weight,
            network,
            webChannel,
            dvdCountry,
            externals,
            image,
            summary,
            updated,
            links
        )
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            show.get("id"),
            show.get("url"),
            show.get("name"),
            show.get("type"),
            show.get("language"),

            json.dumps(show.get("genres")),

            show.get("status"),
            show.get("runtime"),
            show.get("averageRuntime"),
            show.get("premiered"),
            show.get("ended"),
            show.get("officialSite"),

            json.dumps(show.get("schedule")),

            show.get("rating", {}).get("average"),
            show.get("weight"),

            json.dumps(show.get("network")),
            json.dumps(show.get("webChannel")),
            json.dumps(show.get("dvdCountry")),
            json.dumps(show.get("externals")),
            json.dumps(show.get("image")),

            show.get("summary"),

            show.get("updated"),

            json.dumps(show.get("_links"))
        ))

        inserted_count += 1

    connection.commit()
    connection.close()

    print(f"{inserted_count} records inserted successfully!")

else:
    print("Failed to fetch data")
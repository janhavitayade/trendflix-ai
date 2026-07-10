import sqlite3

connection = sqlite3.connect("database/trendflix.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS everything (
    id INTEGER PRIMARY KEY,
    url TEXT,
    name TEXT,
    type TEXT,
    language TEXT,
    genres TEXT,
    status TEXT,
    runtime INTEGER,
    averageRuntime INTEGER,
    premiered TEXT,
    ended TEXT,
    officialSite TEXT,
    schedule TEXT,
    rating REAL,
    weight INTEGER,
    network TEXT,
    webChannel TEXT,
    dvdCountry TEXT,
    externals TEXT,
    image TEXT,
    summary TEXT,
    updated INTEGER,
    links TEXT
)
""")

connection.commit()
connection.close()

print("Everything table created successfully!")
# made the database trendflix.db and created the table shows with the required columns

import sqlite3
connection = sqlite3.connect("database/trendflix.db")  #creates trendflix.db

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS shows (
    id INTEGER PRIMARY KEY,
    name TEXT,
    language TEXT,
    status TEXT,
    premiered TEXT,
    ended TEXT,
    weight INTEGER
)
""")

#snapshot table to track history
cursor.execute("""
CREATE TABLE IF NOT EXISTS snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id INTEGER,
    weight INTEGER,
    rating REAL,
    collected_at TEXT,
    FOREIGN KEY (show_id) REFERENCES shows(id)
)
""")

connection.commit()

connection.close()

print("Database and table created successfully!")
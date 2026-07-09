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

connection.commit()

connection.close()

print("Database and table created successfully!")
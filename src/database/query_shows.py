# This script queries the 'shows' table in the 'trendflix.db' SQLite database and retrieves the top 10 shows based on their weight.
#  It connects to the database, executes a SQL query to fetch the required data, and prints the results in descending order of weight.

import sqlite3

connection = sqlite3.connect("database/trendflix.db")

cursor = connection.cursor()

cursor.execute("""
SELECT id, name, weight
FROM shows
ORDER BY weight DESC
LIMIT 10
""")

results = cursor.fetchall()

print("\nTop 10 Shows by Weight:\n")

for row in results:
    print(row)

connection.close()
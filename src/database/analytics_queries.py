import sqlite3

connection = sqlite3.connect("database/trendflix.db")
cursor = connection.cursor()

cursor.execute("""
SELECT COUNT(*)
FROM shows
""")

result = cursor.fetchone()

print("Total Shows:")
print(result[0])

#---------------to get average weight---------------------------------
cursor.execute("""
SELECT AVG(weight)
FROM shows
""")

result = cursor.fetchone()

print("\nAverage Weight:")
print(round(result[0], 2))
#--------------to get maximum weight----------------------------------
cursor.execute("""
SELECT MAX(weight)
FROM shows
""")

result = cursor.fetchone()

print("\nMaximum Weight:")
print(result[0])
#----------------to get shows with maximum weight--------------------------------
cursor.execute("""
SELECT name, weight
FROM shows
WHERE weight = 100
""")

results = cursor.fetchall()

print("\nShows With Maximum Weight:")

for row in results:
    print(row)
#--------------------to get NULL ratings from snapshots table----------------------------
cursor.execute("""
SELECT *
FROM snapshots
WHERE rating IS NULL
""")

results = cursor.fetchall()

print("\nShows With NULL ratings: ")

for row in results:
    print(row)

#--------------------to get top 10 highest rated shows by using joins--------------------------------
cursor.execute("""
SELECT
    shows.name,
    snapshots.rating
FROM shows
INNER JOIN snapshots
ON shows.id = snapshots.show_id
WHERE snapshots.rating IS NOT NULL
ORDER BY snapshots.rating DESC
LIMIT 10
""")

results = cursor.fetchall()

print("\nTop 10 Highest Rated Shows:")

for row in results:
    print(row)

#--------------------to get top 10 languages with most shows--------------------------------
cursor.execute("""
SELECT
    language,
    COUNT(*) as total_shows
FROM shows
GROUP BY language
ORDER BY total_shows DESC
LIMIT 10
""")

results = cursor.fetchall()

print("\nTop Languages:")

for row in results:
    print(row)

#--------------------to get show status distribution--------------------------------
cursor.execute("""
SELECT
    status,
    COUNT(*) as total
FROM shows
GROUP BY status
ORDER BY total DESC
""")

results = cursor.fetchall()

print("\nShow Status Distribution:")

for row in results:
    print(row)
#--------------------to get total snapshots--------------------------------
import sqlite3

connection = sqlite3.connect("database/trendflix.db")
cursor = connection.cursor()

cursor.execute("""
SELECT COUNT(*)
FROM snapshots
""")

result = cursor.fetchone()

print("\nTotal Snapshots:")
print(result[0])

#--------------------to get first 5 shows--------------------------------
cursor.execute("""
SELECT *
FROM shows
LIMIT 5
""")

results = cursor.fetchall()

for row in results:
    print(row)

#--------------------to get average, minimum, and maximum ratings--------------------------------
cursor.execute("""
SELECT
    AVG(rating),
    MIN(rating),
    MAX(rating)
FROM snapshots
WHERE rating IS NOT NULL
""")
print("\nAverage, Minimum, and Maximum Ratings:")
print(cursor.fetchone())

#--------------------to get premiered dates of first 10 shows--------------------------------
cursor.execute("""
SELECT premiered
FROM shows
LIMIT 10
""")

results = cursor.fetchall()

print("\nPremiered Dates:")

for row in results:
    print(row)
#--------------------to get distinct show statuses--------------------------------
cursor.execute("""
SELECT DISTINCT status
FROM shows
""")

results = cursor.fetchall()

for row in results:
    print(row)
#--------------------to get show IDs with NULL ratings--------------------------------
cursor.execute("""
SELECT show_id
FROM snapshots
WHERE rating IS NULL
""")

results = cursor.fetchall()

for row in results:
    print(row)

#--------------------to get shows with NULL runtime--------------------------------
print("\nShows with NULL runtime:")
cursor.execute("""
SELECT name,runtime
FROM everything
WHERE runtime IS NULL
""")

results = cursor.fetchall()

for row in results:
    print(row)
#--------------------to get shows with NULL averageRuntime--------------------------------
print("\nShows with NULL averageRuntime:")
cursor.execute("""
SELECT name,averageRuntime
FROM everything
WHERE averageRuntime IS NULL
""")

results = cursor.fetchall()

for row in results:
    print(row)
#--------------------to get show 5 genres--------------------------------
print("\nFirst 5 Shows and Their Genres:")
cursor.execute("""
SELECT name, genres
FROM everything
LIMIT 5
""")

results = cursor.fetchall()

for row in results:
    print(row)

connection.close()


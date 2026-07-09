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

connection.close()

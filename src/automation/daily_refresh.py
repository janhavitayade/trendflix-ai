import subprocess

print("=" * 50)
print("TREND FLIX DAILY REFRESH PIPELINE")
print("=" * 50)


# --------------------------------------------------
# STEP 1 - UPDATE EVERYTHING TABLE
# --------------------------------------------------

print("\n[1/2] Updating everything table...")

subprocess.run(
    [
        "python",
        "src/database/insert_everything_into_table_everything.py"
    ],
    check=True
)

print("✓ Everything table updated")

# --------------------------------------------------
# STEP 2 - INSERT SNAPSHOTS
# --------------------------------------------------

print("\n[2/2] Creating historical snapshots...")

subprocess.run(
    [
        "python",
        "src/database/insert_snapshots.py"
    ],
    check=True
)

print("✓ Snapshots updated")

print("\n" + "=" * 50)
print("DAILY REFRESH COMPLETED SUCCESSFULLY")
print("=" * 50)
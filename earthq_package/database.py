"""
database.py - Creates and populates the SQLite earthquake database. We created a separate py file
for this task to make it cleaner and easier to read.

SQLite is a lightweight database that stores everything in a single
local file called earthquakes.db. No server setup is needed.
"""

import sqlite3
from earthq_package.earthquakes import gather_earthquakes


def create_earthquake_db(days):
    """
    Fetch earthquake data from INGV and store it in a local SQLite database.

    This function:
      1. Calls gather_earthquakes() to fetch fresh data from INGV
      2. Creates earthquakes.db if it doesn't exist yet
      3. Creates the table earthquakes_db if it doesn't exist yet
      4. Clears any old data so we don't accumulate duplicates
      5. Inserts all freshly fetched earthquakes

    Args:
        days (int): Number of past days to query from INGV.
    """
    # fetch data from INGV using gather_earthquakes function
    earthquakes = gather_earthquakes(days)

    # connect to the database file
    # if earthquakes.db doesn't exist yet, sqlite3 creates it automatically
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    # create the table if it doesn't already exist
    # TEXT = string, REAL = decimal number
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS earthquakes_db (
            day        TEXT,
            time       TEXT,
            mag        REAL,
            latitude   REAL,
            longitude  REAL,
            place      TEXT
        )
    """
    cursor.execute(create_table_sql)
    conn.commit()

    # delete old rows to avoid duplicates on repeated runs
    cursor.execute("DELETE FROM earthquakes_db")

    # insert all tuples at once
    # the ? placeholders are replaced with values from each tuple
    # each tuple is: (day, time, magnitude, latitude, longitude, place)
    cursor.executemany(
        "INSERT INTO earthquakes_db VALUES (?, ?, ?, ?, ?, ?)",
        earthquakes
    )
    conn.commit()

    # always close connection when done
    cursor.close()
    conn.close()

    print(f"Database populated with {len(earthquakes)} earthquakes.")
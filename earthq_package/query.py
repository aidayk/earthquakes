"""
query.py - Queries the earthquake database and formats output.
"""

import sqlite3


def query_db(K, days, min_magnitude):
    """
    Query the local SQLite database for the strongest recent earthquakes.

    Since the database is already built with only the requested date range,
    we just filter by magnitude, sort by strongest first, and limit to K.

    Args:
        K (int): Maximum number of results to return.
        days (int): Kept as parameter for consistency, date range is
                    already handled when the DB was built.
        min_magnitude (float): Only include earthquakes at least this strong.

    Returns:
        list of tuple: Up to K rows sorted by decreasing magnitude.
            Each tuple: (day, time, mag, latitude, longitude, place)
    """
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    query_sql = """
        SELECT day, time, mag, latitude, longitude, place
        FROM earthquakes_db
        WHERE mag >= ?
        ORDER BY mag DESC
        LIMIT ?
    """

    cursor.execute(query_sql, (min_magnitude, K))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


def print_earthquakes(earthquakes):
    """
    Print earthquake results in a human-readable format.

    Args:
        earthquakes (list of tuple): Each tuple is
            (day, time, mag, latitude, longitude, place)

    Example output line:
        day: 09/01/2025, time: 02:55:45, magnitude: 4.0,
        lat: 40.823, lon: 14.137, place: Campi Flegrei
    """
    if not earthquakes:
        print("No earthquakes found matching your criteria.")
        return

    for eq in earthquakes:
        day, time, mag, lat, lon, place = eq
        print(
            f"day: {day}, time: {time}, magnitude: {mag}, "
            f"lat: {lat}, lon: {lon}, place: {place}"
        )
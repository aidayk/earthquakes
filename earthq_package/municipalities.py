"""
municipalities.py - Finds the closest Italian municipalities to a given
earthquake epicenter.

This module implements Add-On 1: for each earthquake reported by the
program, it computes the 5 nearest municipalities to the epicenter.
"""

import csv
import math
from pathlib import Path

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Compute the distance in kilometers between two points on Earth,
    given their latitude and longitude in decimal degrees.

    We use the haversine formula instead of plain Pythagorean distance
    because the Earth is a sphere, not a flat plane. On a flat plane,
    1 degree of longitude is always the same distance, but on a sphere
    it shrinks the further you are from the equator (e.g. near the poles
    a degree of longitude is almost 0 km). The haversine formula
    accounts for this curvature correctly.

    Args:
        lat1, lon1 (float): Coordinates of the first point.
        lat2, lon2 (float): Coordinates of the second point.

    Returns:
        float: Distance between the two points in kilometers.
    """
    # Earth's average radius in kilometers — this is a standard constant
    EARTH_RADIUS_KM = 6371.0

    # The formula works in radians, not degrees, so we convert first
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences between the two points, in radians
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # This is the core haversine formula. It computes the square of half
    # the chord length between the two points on the sphere's surface.
    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )

    # Convert the chord length into an angular distance (in radians),
    # then into an actual arc distance by multiplying by Earth's radius.
    # We use atan2 instead of asin because it is numerically more stable
    # and handles all angle ranges correctly.
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c

def load_municipalities(filepath=None):
    """
    Load all Italian municipalities from the comuni.csv file.

    Args:
        filepath (str or Path, optional): Path to the CSV file.
            Defaults to comuni.csv inside this package's folder.

    Returns:
        list of tuple: Each tuple is (name, latitude, longitude).
    """
    if filepath is None:
        # By default, look for comuni.csv right next to this script,
        # the same pattern used in earthquakes.py for bounding_box.csv
        filepath = Path(__file__).with_name("comuni.csv")

    municipalities = []

    with open(filepath, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["comune"]
            lat = float(row["lat"])
            lon = float(row["long"])
            municipalities.append((name, lat, lon))

    return municipalities


def find_closest_municipalities(eq_lat, eq_lon, municipalities, top_n=5):
    """
    Find the top_n municipalities closest to a given earthquake epicenter.

    Args:
        eq_lat (float): Latitude of the earthquake epicenter.
        eq_lon (float): Longitude of the earthquake epicenter.
        municipalities (list of tuple): Output of load_municipalities(),
            i.e. a list of (name, lat, lon) tuples.
        top_n (int): How many closest municipalities to return (default 5).

    Returns:
        list of tuple: top_n tuples of (name, distance_km), sorted by
            increasing distance (closest first).
    """
    # Step 1: compute the distance from the epicenter to every municipality
    # We build a list of (name, distance) pairs
    distances = [
        (name, haversine_distance(eq_lat, eq_lon, lat, lon))
        for name, lat, lon in municipalities
    ]

    # Step 2: sort the list by distance, smallest first (closest first)
    # The key=lambda tells sort to compare using the second element (distance)
    distances.sort(key=lambda pair: pair[1])

    # Step 3: take only the first top_n entries (the closest ones)
    return distances[:top_n]
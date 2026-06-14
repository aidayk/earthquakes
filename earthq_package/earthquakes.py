"""
earthquakes.py - Functions for gathering earthquake data from the INGV API.
"""

import csv
import datetime
from pathlib import Path

import requests


INGV_URL = "https://webservices.ingv.it/fdsnws/event/1/query"


def read_bounding_box():
    """Read the Italian bounding box coordinates from bounding_box.csv."""
    csv_path = Path(__file__).with_name("bounding_box.csv")

    with csv_path.open("r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)

    return {
        "minlatitude": float(row["minlatitude"]),
        "maxlatitude": float(row["maxlatitude"]),
        "minlongitude": float(row["minlongitude"]),
        "maxlongitude": float(row["maxlongitude"]),
    }


def _format_datetime_parts(time_string):
    """Convert an ISO datetime string into day and time strings."""
    clean_time = time_string.replace("Z", "+00:00")
    event_datetime = datetime.datetime.fromisoformat(clean_time)

    day = event_datetime.strftime("%d/%m/%Y")
    time = event_datetime.strftime("%H:%M:%S")

    return day, time


def gather_earthquakes(days):
    """
    Query the INGV API and return earthquakes inside the Italian bounding box.

    Returns:
        list[tuple]: tuples with day, time, magnitude, latitude, longitude, place.
    """
    bounding_box = read_bounding_box()

    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(days=days)

    params = {
        "format": "text",
        "starttime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "minlatitude": bounding_box["minlatitude"],
        "maxlatitude": bounding_box["maxlatitude"],
        "minlongitude": bounding_box["minlongitude"],
        "maxlongitude": bounding_box["maxlongitude"],
    }

    response = requests.get(INGV_URL, params=params, timeout=30)
    response.raise_for_status()

    lines = response.text.strip().splitlines()

    if not lines:
        return []

    header = lines[0].lstrip("#").split("|")
    earthquakes = []

    for line in lines[1:]:
        values = line.split("|")
        event = dict(zip(header, values))

        try:
            day, time = _format_datetime_parts(event["Time"])
            magnitude = float(event["Magnitude"])
            latitude = float(event["Latitude"])
            longitude = float(event["Longitude"])
            place = event.get("EventLocationName", "")
        except (KeyError, TypeError, ValueError):
            continue

        earthquakes.append(
            (day, time, magnitude, latitude, longitude, place)
        )

    return earthquakes
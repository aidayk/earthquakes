"""
test_project.py - Unit tests for the earthquake project.

Run with:
    python -m unittest test_project -v
"""

from unittest import TestCase
from earthq_package.earthquakes import read_bounding_box
from earthq_package.database import create_earthquake_db
from earthq_package.query import query_db
import sqlite3

class TestEarthquakeProject(TestCase):
    """Test suite for the earthquake query application."""

    @classmethod
    def setUpClass(cls):
        """
        Runs once before all tests start.

        Builds the database so every test below can use it.
        We use 30 days so there is enough data to test with.
        """
        create_earthquake_db(days=30)

    def test_bounding_box(self):
        """
        Test that Padova, Palermo and Parma fall inside the bounding box.

        We check all three cities because they cover different parts
        of Italy — north, south, and a major island (Sicily).

        Coordinates used:
          Padova:  lat=45.41, lon=11.88  (northeast)
          Palermo: lat=38.12, lon=13.36  (Sicily)
          Parma:   lat=44.80, lon=10.33  (north)
        """
        bbox = read_bounding_box()

        cities = {
            'Padova':  (45.41, 11.88),
            'Palermo': (38.12, 13.36),
            'Parma':   (44.80, 10.33),
        }

        for city, (lat, lon) in cities.items():
            self.assertGreaterEqual(
                lat, bbox['minlatitude'],
                msg=f"{city} latitude {lat} is below minlatitude {bbox['minlatitude']}"
            )
            self.assertLessEqual(
                lat, bbox['maxlatitude'],
                msg=f"{city} latitude {lat} is above maxlatitude {bbox['maxlatitude']}"
            )
            self.assertGreaterEqual(
                lon, bbox['minlongitude'],
                msg=f"{city} longitude {lon} is left of minlongitude {bbox['minlongitude']}"
            )
            self.assertLessEqual(
                lon, bbox['maxlongitude'],
                msg=f"{city} longitude {lon} is right of maxlongitude {bbox['maxlongitude']}"
            )

    def test_magnitude(self):
        """
        Test that no earthquake in the DB has magnitude above 9.5.

        9.5 was the magnitude of the 1960 Valdivia earthquake in Chile,
        the strongest ever recorded. Nothing should exceed this.
        """
        conn = sqlite3.connect('earthquakes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(mag) FROM earthquakes_db")
        max_mag = cursor.fetchone()[0]
        conn.close()

        if max_mag is not None:  # skip check if database is empty
            self.assertLessEqual(
                max_mag, 9.5,
                msg=f"Database contains magnitude {max_mag} which exceeds the maximum ever recorded!"
            )

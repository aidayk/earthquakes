"""
write_bounding_box.py - Create the CSV file containing the Italian bounding box.
"""

import csv
from pathlib import Path


BOUNDING_BOX = {
    "minlatitude": 35.0,
    "maxlatitude": 47.5,
    "minlongitude": 5.0,
    "maxlongitude": 20.0,
}


def write_bounding_box():
    """Write the Italian bounding box coordinates to bounding_box.csv."""
    output_path = Path(__file__).with_name("bounding_box.csv")

    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=BOUNDING_BOX.keys())
        writer.writeheader()
        writer.writerow(BOUNDING_BOX)


if __name__ == "__main__":
    write_bounding_box()
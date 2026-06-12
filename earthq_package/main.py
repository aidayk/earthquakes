"""
main.py - Entry point for the earthquake query application.

This script reads command-line arguments from the user and runs
the earthquake query program.
"""

import argparse

from earthq_package.earthquakes import get_earthquake


def main():
    parser = argparse.ArgumentParser(
        description="Return earthquake information for a given number of past days."
    )

    parser.add_argument(
        "--days",
        type=int,
        required=True,
        help="Number of past days to query."
    )

    parser.add_argument(
        "--K",
        type=int,
        required=True,
        help="Maximum number of earthquakes to return."
    )

    parser.add_argument(
        "--magnitude",
        type=float,
        required=True,
        help="Minimum earthquake magnitude."
    )

    args = parser.parse_args()

    mag, place = get_earthquake(args.days)

    print(
        "The largest earthquake of last {} days had magnitude {} and was located at {}".format(
            args.days, mag, place
        )
    )

    print("Requested maximum number of earthquakes:", args.K)
    print("Requested minimum magnitude:", args.magnitude)


if __name__ == "__main__":
    main()
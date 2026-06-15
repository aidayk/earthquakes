"""
main.py - Entry point for the earthquake query application.

Parses command-line arguments, builds the database from INGV data,
queries it and prints the results.
"""

import argparse
from earthq_package.database import create_earthquake_db
from earthq_package.query import query_db, print_earthquakes

def main():

    """
        Main function - entry point of the program.

        Parses --days, --K and --magnitude from the command line,
        fetches fresh earthquake data from INGV into a local SQLite
        database, then queries and prints the top K results.
    """

    parser = argparse.ArgumentParser(
        description="Return the strongest earthquakes in Italy."
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

    # build/refresh database with data for the requested period
    create_earthquake_db(args.days)

    #query the database and print the results
    results=query_db(args.K,args.days,args.magnitude)
    print_earthquakes(results)


if __name__ == "__main__":
    main()

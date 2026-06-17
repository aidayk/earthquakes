"""
main.py - Entry point for the earthquake query application.

Parses command-line arguments, builds the database from INGV data,
queries it and prints the results.
"""

import argparse
from earthq_package.database import create_earthquake_db
from earthq_package.query import query_db, print_earthquakes
from earthq_package.municipalities import load_municipalities, find_closest_municipalities

def main():

    """
        Main function - entry point of the program.

        Parses --days, --K and --magnitude from the command line,
        fetches fresh earthquake data from INGV into a local SQLite
        database, then queries and prints the top K results.

        If --addon is passed, also prints the 5 closest Italian
        municipalities to each earthquake's epicenter.
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

    # This is our new add-on flag. action="store_true" means the user
    # doesn't pass a value for it - it's just a switch. If present on
    # the command line, args.addon becomes True; otherwise False.
    parser.add_argument(
        "--addon",
        action="store_true",
        help="If set, also show the 5 closest Italian municipalities "
             "to each earthquake's epicenter."
    )

    args = parser.parse_args()

    # build/refresh database with data for the requested period
    create_earthquake_db(args.days)

    #query the database and print the results
    results=query_db(args.K,args.days,args.magnitude)
    print_earthquakes(results)

    # Only do the extra add-on work if the user asked for it.
    # This keeps the normal program fast when the flag isn't used,
    # since loading and scanning thousands of municipalities takes time.
    if args.addon:
        # Load the municipality dataset once, outside the loop below,
        # so we don't re-read the CSV file for every single earthquake
        municipalities = load_municipalities()

        print("\nClosest municipalities for each earthquake")

        for eq in results:
            day, time, mag, lat, lon, place = eq

            closest = find_closest_municipalities(lat, lon, municipalities, top_n=5)

            print(f"\nEarthquake at {place} (magnitude {mag}):")
            for name, distance in closest:
                # :.1f formats the distance to 1 decimal place, e.g. 12.3 km
                print(f"  - {name}: {distance:.1f} km away")


if __name__ == "__main__":
    main()

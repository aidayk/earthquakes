"""
main.py - Entry point for the earthquake query application.

This script reads command-line arguments from the user.
The final earthquake query logic will be connected in the next project steps.
"""

import argparse


def main():
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

    print("Command-line arguments received:")
    print("days:", args.days)
    print("K:", args.K)
    print("magnitude:", args.magnitude)


if __name__ == "__main__":
    main()
"""
main.py - Entry point for the earthquake query application.

Imports the get_earthquake function from the earthquakes module
and prints the result for a given number of past days.
"""

from earthq_package.earthquakes import get_earthquake

def main():
    days = 10
    mag, place = get_earthquake(days)

    print("The largest earthquake of last {} days had magnitude {} and was located at {}".format(days, mag, place))

if __name__ == "__main__":
    main()
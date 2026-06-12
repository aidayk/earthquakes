"""
earthquakes.py - Fetches earthquake data from the USGS database.

USGS (United States Geological Survey) provides a public API
for querying global seismic events.
"""

import requests
import datetime
import json


USGS_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query?starttime={}&format=geojson&limit=20000'

""" 
    Query the USGS database and return the strongest earthquake in the last days_past days.
    Arguments:
    days_past(int): how many days back to search
    Returns:
    tuple: (magnitude, place), where magnitude is a float, place is a string describing a location.
    For ex., like 7.7 and 124km NNW of Lucea, Jamaica.
"""
def get_earthquake(days_past):
    #get the date of today - days_past days at 00 AM
    start_date = (datetime.datetime.now() + datetime.timedelta(days=-days_past)).strftime("%Y-%m-%d")
    url = USGS_URL.format(start_date)
    r = requests.get(url)
    # Parse the JSON response
    events = json.loads(requests.get(url).text)
    magnitude = 0
    place = ''
    # Loop through all events to find the one with highest magnitude
    for event in events['features']:
        try:
            mag = float(event['properties']['mag'])
        except TypeError:
            pass    # skip events with missing magnitude data
        if mag > magnitude:
            magnitude = mag
            place = event['properties']['place']
    return magnitude, place
"""
This script downloads Google Street View images for multiple countries using a list of coordinates and the Google Maps
Street View API.
"""

import os
import json
import random
from dotenv import load_dotenv

# Files
import downloadImages2

# Load environment variables from .env file
load_dotenv()

# Set request standard parameters
api_key = os.getenv('STREET_VIEW_API_KEY_EBBE')
size = "224x224"
pitch = 0
fov = 120
source = "outdoor"
index = 0
sizes = [50, 100, 200, 300, 400, 500]

# Load country-radius data from JSON file
with open('./ireland.json', 'r') as f:
    country_search_radius = json.load(f)

# Load coordinates data from JSON file
with open('./coordinates.json', 'r') as f:
    coordinates = json.load(f)

print("Reading radius dictionary...")
for country in coordinates:
    # Get the radius for this country
    radius = next((c['radius'] for c in country_search_radius if c['name'] == country), None)

    # Loop through the coordinates and download images
    for lat, lon in coordinates[country]:
        heading = random.randint(0, 359)
        index += 1
        # Construct the Google Maps Street View API request URL
        url = f"https://maps.googleapis.com/maps/api/streetview?size={size}&location={lat},{lon}&heading={heading} \
            &pitch={pitch}&fov={fov}&radius={radius}&source={source}&key={api_key} "

        # Download and save images for the current coordinate
        downloadImages2.download_images(country, url, size, '../../data/countries/testing/224x224')

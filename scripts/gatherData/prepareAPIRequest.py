import os
import json
import random

from dotenv import load_dotenv

# This script downloads Google Street View images for multiple countries
# using a list of coordinates and the Google Maps Street View API.

# Files
import downloadImages

# Load environment variables from .env file
load_dotenv()

# Set request standard parameters
api_key = os.getenv('STREET_VIEW_API_KEY')
size = "1000x1000"
pitch = 0
fov = 120
source = "outdoor"
index = 0
sizes = [50, 100, 200, 300, 400, 500]

# Load country-radius data from JSON file
with open('./countries_and_search_radius.json', 'r') as f:
    country_search_radius = json.load(f)

# Load coordinates data from JSON file
with open('../play/game1.json', 'r') as f:
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
        downloadImages.download_images(index, country, url, sizes)

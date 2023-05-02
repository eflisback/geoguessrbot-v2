"""
This script downloads Google Street View images for multiple cells using a list of coordinates and the Google Maps
Street View API.
"""

import os
import json
import random
from dotenv import load_dotenv

# Files
import downloadImages

# Load environment variables from .env file
load_dotenv()

# Set request standard parameters
api_key = os.getenv('STREET_VIEW_API_KEY')
size = "224x224"
pitch = 0
fov = 120
source = "outdoor"

# Load coordinates for each cell from JSON file
with open('./cellCoordinates.json', 'r') as f:
    coordinates = json.load(f)


for cell in coordinates:
    # Loop through the coordinates and download images
    index = 0
    for lat, lon in coordinates[cell]:
        heading = random.randint(0, 359)
        index += 1
        # Construct the Google Maps Street View API request URL
        url = f"https://maps.googleapis.com/maps/api/streetview?size={size}&location={lat},{lon}&heading={heading} \
            &pitch={pitch}&fov={fov}&radius=300000&source={source}&key={api_key} "

        # Download and save images for the current coordinate
        downloadImages.download_images(index, cell, url, size)

    print("\n")

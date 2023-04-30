"""
This script organizes images in a specified directory into subdirectories based on the country name extracted from the
image filenames. It first creates a set of unique country classes and then creates a subdirectory for each country. The
script then moves each image to its corresponding country subdirectory.
"""

import os
import shutil

country_position = 1  # The part of file-name which is country
data_dir = "../../data/toBeAdded/1000x1000"
country_classes = set()

# Get a set of all country classes
for file in os.listdir(data_dir):
    if file.endswith('.jpg'):
        country = file.split('_')[country_position]
        country_classes.add(country)

# Create a subdirectory for each country class
for country in country_classes:
    os.makedirs(os.path.join(data_dir, country), exist_ok=True)

# Move each image to its corresponding country subdirectory
for file in os.listdir(data_dir):
    if file.endswith('.jpg'):
        print("moved one file...")
        country = file.split('_')[country_position]
        src_path = os.path.join(data_dir, file)
        dst_path = os.path.join(data_dir, country, file)
        shutil.move(src_path, dst_path)

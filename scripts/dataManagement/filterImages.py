"""
This script identifies and removes images identical to a specified error-image from a given directory and its
subdirectories. It converts both the error-image and each encountered image to numpy arrays and checks if their pixel
values are identical. If they match, the script deletes the matching image.
"""

import os
import numpy as np
from PIL import Image

# Set the path to the known error-image
error_image_path = "../../data/countries/training/224x224_balanced/albania/684_albania_224x224RWW.jpg"

# Open the error-image and convert it to a numpy array
with Image.open(error_image_path) as img:
    error_array = np.array(img)

# Set the directory path
dir_path = "../../data/countries/training/224x224_balanced"

# Traverse all subdirectories within the directory
for subdir, dirs, files in os.walk(dir_path):
    # Loop through each file in the subdirectory
    for filename in files:
        file_path = os.path.join(subdir, filename)

        # Skip any non-JPEG files
        if not file_path.endswith(".jpg"):
            continue

        # Open the image file and convert it to a numpy array
        with Image.open(file_path) as img:
            img_array = np.array(img)

            # Check if the pixel values are identical to the error-image
            if np.array_equal(img_array, error_array):
                # If the pixel values are identical, delete the file
                print("Removed ", filename)
                os.remove(file_path)

import os
import numpy as np
from PIL import Image

# Set the path to the known error-image
error_image_path = "/path/to/error-image.jpg"

# Open the error-image and convert it to a numpy array
with Image.open(error_image_path) as img:
    error_array = np.array(img)

# Set the directory path
dir_path = "/path/to/folder"

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
                os.remove(file_path)

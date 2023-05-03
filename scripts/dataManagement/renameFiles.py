"""
This script renames image files within subdirectories of a specified base directory. It iterates through each
subdirectory, and for each JPEG file, constructs a new filename based on a counter, the subdirectory name, and a
pre-defined suffix. The script then renames the file with the new filename and increments the counter for the next file.
"""

import os

# Set the base path for the directory containing the subdirectories
base_path = "../../data/grid/training"

# Loop through each subdirectory
for subdir in os.listdir(base_path):
    subdir_path = os.path.join(base_path, subdir)

    # Skip any files that are not directories
    if not os.path.isdir(subdir_path):
        continue

    # Set the starting number for the file names
    file_number = 1

    # Loop through each file in the subdirectory
    for filename in os.listdir(subdir_path):
        file_path = os.path.join(subdir_path, filename)

        # Skip any non-JPEG files
        if not file_path.endswith(".jpg"):
            continue

        # Construct the new file name and rename the file
        new_filename = "{}_{}_{}.jpg".format(file_number, subdir, "224x224R")
        new_file_path = os.path.join(subdir_path, new_filename)
        os.rename(file_path, new_file_path)

        # Increment the file number for the next file
        file_number += 1

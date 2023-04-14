import os
from PIL import Image

# Set the directory path
dir_path = "../data/training/224x224"

# Loop through each subdirectory
for subdir in os.listdir(dir_path):
    subdir_path = os.path.join(dir_path, subdir)

    # Skip any files that are not directories
    if not os.path.isdir(subdir_path):
        continue

    # Loop through each file in the subdirectory
    for filename in os.listdir(subdir_path):
        if not filename.startswith("resized"):
            file_path = os.path.join(subdir_path, filename)
            print("Removed ",  filename)
            os.remove(file_path)

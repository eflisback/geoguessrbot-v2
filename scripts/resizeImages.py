import os
from PIL import Image

# Set the directory path
dir_path = "../toBeResized"

# Set the target image size
target_size = (224, 224)

# Loop through each subdirectory
for subdir in os.listdir(dir_path):
    subdir_path = os.path.join(dir_path, subdir)

    # Skip any files that are not directories
    if not os.path.isdir(subdir_path):
        continue

    # Loop through each file in the subdirectory
    for filename in os.listdir(subdir_path):
        file_path = os.path.join(subdir_path, filename)

        # Skip any non-JPEG files
        if not file_path.endswith(".jpg"):
            continue

        # Open the image file and resize it
        with Image.open(file_path) as img:
            img = img.resize(target_size)

            # Save the resized image
            resized_path = os.path.join(subdir_path, "resized_" + filename)
            img.save(resized_path)

import os
import requests


def download_images(cell, url, size, base_dir):
    # Create directory structure if it doesn't exist
    os.makedirs(os.path.join(base_dir, "training"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "training", cell), exist_ok=True)

    # Count existing files in sub-directory to determine start value for index
    existing_files = os.listdir(os.path.join(base_dir, "training", cell))
    index_start = len(existing_files) + 1

    # Send request to Street View API and download image
    response = requests.get(url)
    image_data = response.content

    # Save image to file
    filename = f"{index_start}_{cell}_{size}.jpg"
    filepath = os.path.join(base_dir, "training", cell, filename)
    with open(filepath, "wb") as f:
        f.write(image_data)

    # Print progress message
    print(f"Downloaded image {index_start} for cell {cell}.")

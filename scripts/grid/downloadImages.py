import os
import requests


def download_images(index, cell, url, size):
    # Create directory structure if it doesn't exist
    os.makedirs("training", exist_ok=True)
    os.makedirs(os.path.join("training", cell), exist_ok=True)

    # Send request to Street View API and download image
    response = requests.get(url)
    image_data = response.content

    # Save image to file
    filename = f"{index}_{cell}_{size}.jpg"
    filepath = os.path.join("training", cell, filename)
    with open(filepath, "wb") as f:
        f.write(image_data)

    # Print progress message
    print(f"Downloaded image {index} for cell {cell}.")

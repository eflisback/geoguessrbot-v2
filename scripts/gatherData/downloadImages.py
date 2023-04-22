import os
import requests
from PIL import Image
from bcolors import BColors

# This script downloads images of different sizes from a given URL,
# resizes them, and saves them to separate folders based on their size.


def download_images(i, country, u, sizes):
    # Send request
    response = requests.get(u)
    print("\n", i, f"{BColors.WARNING}API request sent...{BColors.ENDC}")

    # Specify folder path and create folder if it doesn't exist
    folder_path = os.path.join(os.path.dirname(__file__), "../../data/toBeAdded/1000x1000")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save 1000x1000 image to folder
    with open(os.path.join(folder_path, f"{i}_{country}_1000x1000.jpg"), "wb") as f:
        f.write(response.content)
    print(f"{BColors.OKGREEN}   1000x1000 image downloaded and saved...{BColors.ENDC}")

    # Open image file with Pillow
    image = Image.open(os.path.join(folder_path, f"{i}_{country}_1000x1000.jpg"))

    for size in sizes:
        # Resize image to specified size
        new_image = image.resize((size, size))

        # Specify folder path and create folder if it doesn't exist
        folder_path = os.path.join(os.path.dirname(__file__), f"../../data/toBeAdded/{size}x{size}")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Save resized image to folder
        new_image.save(os.path.join(folder_path, f"{i}_{country}_{size}x{size}.jpg"))
        print(f"{BColors.OKGREEN}       {size}x{size} image created and saved...{BColors.ENDC}")

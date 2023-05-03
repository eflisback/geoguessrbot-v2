import json
import os
import numpy as np
import requests
from PIL import Image
from dotenv import load_dotenv
from keras.models import load_model

# Load API key from .env file
load_dotenv(dotenv_path='../../../.env')
api_key = os.getenv('STREET_VIEW_API_KEY')

# Load the trained model
model = load_model('../../../models/grid/GriddaBriddaMk1.h5')

# Parameters for Street View API
size = "224x224"
pitch = "0"
fov = "120"
radius = "1000"
source = "outdoor"

# Create gameImages folder if it doesn't exist
game_images_folder = 'gameImages'
if not os.path.exists(game_images_folder):
    os.makedirs(game_images_folder)

lat, lon, heading = input("Enter latitude, longitude, and heading separated by commas. \n").split(',')

# Download Street View image
url = f"https://maps.googleapis.com/maps/api/streetview?size={size}&location={lat}," \
     f"{lon}&heading={heading}&pitch={pitch}&fov={fov}&radius={radius}&source={source}&key={api_key}"
response = requests.get(url)

# Save the image in gameImages folder
image_path = os.path.join(game_images_folder, 'image.jpg')
with open(image_path, 'wb') as f:
    f.write(response.content)


# Read the image and preprocess it
input_image_path = './gameImages/image.jpg'
image = Image.open(input_image_path)

image_array = np.array(image)
image_array = np.expand_dims(image_array, axis=0)

# Make predictions using the model
predictions = model.predict(image_array)

# Get country class names from the training data directory
training_data_dir = '../../../data/grid/training'
class_names = [dir_name for dir_name in os.listdir(training_data_dir) if
               os.path.isdir(os.path.join(training_data_dir, dir_name))]

# Create a list of tuples containing class names and their corresponding confidence levels
class_confidence_list = [(cell, predictions[0][i]) for i, cell in enumerate(class_names)]

# Sort the list in descending order based on the confidence levels
class_confidence_list.sort(key=lambda x: x[1], reverse=True)

# Print the class names and their corresponding confidence levels in descending order
for cell, confidence in class_confidence_list:
    print(f"{cell}: {confidence}")

# Extract the confidence levels for each cell
cell_confidence_levels = {cell: confidence for cell, confidence in class_confidence_list}

# Read the JSON file with the cell coordinates
with open('../../../scripts/grid/filtered_grid.json', 'r') as f:
    cell_coordinates = json.load(f)

# Calculate the center coordinate for each cell and store them with their confidence levels
cell_centers_confidence = {}
for cell, coordinates in cell_coordinates.items():
    center_lat = (coordinates['max_lat'] + coordinates['min_lat']) / 2
    center_lon = (coordinates['max_lon'] + coordinates['min_lon']) / 2
    cell_centers_confidence[cell] = {
        "center": (center_lat, center_lon),
        "confidence": cell_confidence_levels[cell]
    }

# Calculate the weighted average of the center coordinates using the confidence levels
total_confidence = sum(cell_confidence_levels.values())
weighted_lat = sum(center["center"][0] * center["confidence"] for center in cell_centers_confidence.values()) / total_confidence
weighted_lon = sum(center["center"][1] * center["confidence"] for center in cell_centers_confidence.values()) / total_confidence

weighted_coordinate = (weighted_lat, weighted_lon)

print("Weighted Coordinate:", weighted_coordinate)

"""
Play GeoGuessr with trained model

This script downloads and displays Google Street View images based on the user's input of latitude, longitude,
and heading. It then uses a trained model to predict the country the image is from and displays the top three
guesses along with their probabilities.
"""

import os
import requests
from io import BytesIO
import numpy as np
import tensorflow as tf
from PIL import Image
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# Load API key from .env file
load_dotenv(dotenv_path='../../../.env')
api_key = os.getenv('STREET_VIEW_API_KEY')

# Load the pre-trained model
model_path = '../../../models/countries/HittaBrittaMk4.h5'
model = tf.keras.models.load_model(model_path)

# Get country class names from the training data directory
training_data_dir = '../../../data/countries/training/224x224_balanced'
class_names = [dir_name for dir_name in os.listdir(training_data_dir) if
               os.path.isdir(os.path.join(training_data_dir, dir_name))]

# Parameters for Street View API
size = "1000x1000"
pitch = "0"
fov = "120"
radius = "1000"
source = "outdoor"

# Create gameImages folder if it doesn't exist
game_images_folder = 'gameImages'
if not os.path.exists(game_images_folder):
    os.makedirs(game_images_folder)


# Function to predict the country based on the image data
def predict_country(image_data):
    # Preprocess the image data
    image = Image.open(BytesIO(image_data)).resize((224, 224))
    image_array = np.array(image).reshape((1,) + image.size[::-1] + (3,))

    # Make the prediction
    prediction = model.predict(image_array)
    probabilities = list(prediction[0])
    sorted_indexes = np.argsort(probabilities)[::-1]

    # Get top three predictions
    top_three = [(class_names[index], probabilities[index]) for index in sorted_indexes[:3]]
    return top_three


# Main game loop
for i in range(5):
    lat, lon, heading = input("Enter latitude, longitude, and heading separated by commas. \n").split(',')

    # Download Street View image
    url = f"https://maps.googleapis.com/maps/api/streetview?size={size}&location={lat}," \
          f"{lon}&heading={heading}&pitch={pitch}&fov={fov}&radius={radius}&source={source}&key={api_key}"
    response = requests.get(url)

    # Save the image in gameImages folder
    image_path = os.path.join(game_images_folder, f'image_{i + 1}.jpg')
    with open(image_path, 'wb') as f:
        f.write(response.content)

    # Make prediction
    top_three_guesses = predict_country(response.content)

    # Display the image and top three guesses using matplotlib
    image = Image.open(BytesIO(response.content))

    plt.imshow(image)
    plt.title(f"Round {i + 1} of 5")
    plt.axis('off')

    # Add predictions as text
    result_text = "\n".join([f"{country}: {probability * 100:.2f}%" for country, probability in top_three_guesses])
    plt.text(image.size[0] * 1.1, image.size[1] * 0.5, result_text, fontsize=12, verticalalignment='center')

    plt.show()

    print("\n" + "=" * 40 + "\n")

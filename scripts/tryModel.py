import tensorflow as tf
import numpy as np
from keras.models import load_model
import os

# Load saved model
model = load_model('../models/HittaBrittaMk1.h5')
data_dir = "../data/testing/224x224"

# Set image file path
image_file_path = '../data/testing/224x224/france/2_france_224x224.jpg'

# Load new image in RGB mode
new_image = tf.keras.preprocessing.image.load_img(image_file_path,
                                                  target_size=(224, 224), color_mode='rgb')

# Convert image to numpy array
new_image = tf.keras.preprocessing.image.img_to_array(new_image)

# Reshape image to add batch dimension
new_image = new_image.reshape((1,) + new_image.shape)

# Make prediction using the loaded model
prediction = model.predict(new_image)

# Get list of class names
class_names = sorted(os.listdir(data_dir))

# Get list of probabilities for each class
probabilities = list(prediction[0])

# Sort class names and probabilities in descending order by probability
sorted_classes = [class_names[index] for index in np.argsort(probabilities)[::-1]]
sorted_probabilities = sorted(probabilities, reverse=True)

# Print sorted list of classes and probabilities
for i in range(5):
    print(f"{sorted_classes[i]}: {sorted_probabilities[i] * 100:.2f}%")

# Extract the correct answer from the file path
correct_answer = image_file_path.split('/')[-2]

# Check if correct answer is in top 5 predictions
if correct_answer not in sorted_classes[:5]:
    # Find the rank and confidence of the correct answer
    correct_answer_index = sorted_classes.index(correct_answer)
    correct_answer_rank = correct_answer_index + 1
    correct_answer_confidence = sorted_probabilities[correct_answer_index]

    # Print the rank and confidence of the correct answer
    print(f"The right answer, {correct_answer.capitalize()}, came in {correct_answer_rank}th place with a confidence of {correct_answer_confidence * 100:.2f}%")

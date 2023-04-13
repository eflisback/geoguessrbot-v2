import tensorflow as tf
import numpy as np
from keras.models import load_model
import os

# Load saved model
model = load_model('../models/test.h5')
data_dir = "../data/224x224"

# Load new image in RGB mode
new_image = tf.keras.preprocessing.image.load_img('../../data/testing_224x224/1000x1000/resized_5_austria_1000x1000.jpg',
                                                  target_size=(224, 224), color_mode='rgb')

# Convert image to numpy array
new_image = tf.keras.preprocessing.image.img_to_array(new_image)

# Scale pixel values to [0, 1]
# new_image /= 255.

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
for i in range(len(sorted_classes)):
    print(f"{sorted_classes[i]}: {sorted_probabilities[i]}")

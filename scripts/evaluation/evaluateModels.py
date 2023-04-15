import tensorflow as tf
import numpy as np
from keras.models import load_model
import os
import csv

# Set the models directory and data directory
models_dir = "../../models/"
data_dir = "../../data/training/224x224"
testing_dir = "../../data/testing/224x224"

# Get list of class names
class_names = sorted(os.listdir(data_dir))

# Iterate over all models in the models directory
for model_name in os.listdir(models_dir):
    model_path = os.path.join(models_dir, model_name)

    # Load saved model
    model = load_model(model_path)

    # Print the model name
    print(f"Model: {model_name}")

    # Create a CSV file to store the confidence levels of the correct answers for this model
    csv_filename = f"correct_answers_confidence_{model_name.replace('.h5', '')}.csv"
    with open(csv_filename, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write the CSV header
        csvwriter.writerow(["Image", "Correct_Class", "Confidence"])

        # Iterate over each class subdirectory in the testing directory
        for class_name in class_names:
            class_dir = os.path.join(testing_dir, class_name)

            # Iterate over each image file in the class subdirectory
            for image_name in os.listdir(class_dir):
                image_file_path = os.path.join(class_dir, image_name)

                # Load new image in RGB mode
                new_image = tf.keras.preprocessing.image.load_img(image_file_path,
                                                                  target_size=(224, 224), color_mode='rgb')

                # Convert image to numpy array
                new_image = tf.keras.preprocessing.image.img_to_array(new_image)

                # Reshape image to add batch dimension
                new_image = new_image.reshape((1,) + new_image.shape)

                # Make prediction using the loaded model
                prediction = model.predict(new_image)

                # Get list of probabilities for each class
                probabilities = list(prediction[0])

                # Sort class names and probabilities in descending order by probability
                sorted_classes = [class_names[index] for index in np.argsort(probabilities)[::-1]]
                sorted_probabilities = sorted(probabilities, reverse=True)

                # Print the image file path and sorted list of classes and probabilities
                print(f"Image: {image_file_path}")
                for i in range(5):
                    print(f"{sorted_classes[i]}: {sorted_probabilities[i] * 100:.2f}%")
                print()

                # Extract the correct answer from the file path
                correct_answer = os.path.basename(os.path.dirname(image_file_path))

                # Check if correct answer is in top 5 predictions
                if correct_answer not in sorted_classes[:5]:
                    # Find the rank and confidence of the correct answer
                    correct_answer_index = sorted_classes.index(correct_answer)
                    correct_answer_rank = correct_answer_index + 1
                    correct_answer_confidence = sorted_probabilities[correct_answer_index]

                    # Print the rank and confidence of the correct answer
                    print(f"The right answer, {correct_answer.capitalize()}, came in {correct_answer_rank}th place with a confidence of {correct_answer_confidence * 100:.2f}%")

                # Save the confidence level of the correct answer to the CSV file
                else:
                    correct_answer_index = sorted_classes.index(correct_answer)
                    correct_answer_confidence = sorted_probabilities[correct_answer_index]

                csvwriter.writerow([image_name, correct_answer, correct_answer_confidence])

                print("\n" + "=" * 40 + "\n")

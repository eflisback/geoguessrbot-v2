import pandas as pd
import numpy as np

data = pd.read_csv("../evaluations/csv/correct_answers_confidence_HittaBrittaMk1.csv")

# Group the data by the 'Correct_Class' column, which represents the country
grouped_data = data.groupby('Correct_Class')

# Calculate the mean confidence for each group (country)
mean_confidence_by_country = grouped_data['Confidence'].mean()

# Store the mean confidence values in a dictionary
country_confidence_dict = mean_confidence_by_country.to_dict()


def allocate_images(total_images_to_download, country_confidence_dict):
    # Step 1: Calculate the inverse of the mean confidence for each country
    inverse_confidence = {country: 1 / confidence for country, confidence in country_confidence_dict.items()}

    # Step 2: Normalize these inverse confidence values to make them sum up to 1
    total_inverse_confidence = sum(inverse_confidence.values())
    normalized_inverse_confidence = {country: (value / total_inverse_confidence) for country, value in
                                     inverse_confidence.items()}

    # Step 3: Multiply each normalized value by the total number of images to be downloaded
    images_to_download = {country: int(round(normalized_value * total_images_to_download)) for country, normalized_value
                          in normalized_inverse_confidence.items()}

    return images_to_download


total_images_to_download = 10000
allocated_images = allocate_images(total_images_to_download, country_confidence_dict)
print(allocated_images)

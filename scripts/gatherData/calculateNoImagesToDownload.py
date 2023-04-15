import pandas as pd
import json

data = pd.read_csv("../../evaluations/csv/correct_answers_confidence_HittaBrittaMk2.csv")

grouped_data = data.groupby('Correct_Class')
mean_confidence_by_country = grouped_data['Confidence'].mean()
country_confidence_dict = mean_confidence_by_country.to_dict()


def allocate_images(total_images_to_download, country_confidence_dict):
    inverse_confidence = {country: 1 / confidence for country, confidence in country_confidence_dict.items()}
    total_inverse_confidence = sum(inverse_confidence.values())
    normalized_inverse_confidence = {country: (value / total_inverse_confidence) for country, value in
                                     inverse_confidence.items()}
    images_to_download = {country: int(round(normalized_value * total_images_to_download)) for country, normalized_value
                          in normalized_inverse_confidence.items()}

    return images_to_download


total_images_to_download = 20000
allocated_images = allocate_images(total_images_to_download, country_confidence_dict)

allocated_images_filename = f"allocated_images_{total_images_to_download}.json"
with open(allocated_images_filename, 'w') as outfile:
    json.dump(allocated_images, outfile)

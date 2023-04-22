from generateRandomLatLng import random_points_within_country
import geopandas as gpd
import json
import time
from bcolors import BColors

# This script generates random coordinates within multiple countries,
# loads the countries' shapefiles, and saves the coordinates to a single JSON file.


def get_coordinate_list(c, c_s, n):
    # Print status message and start timer
    print(f"{BColors.OKBLUE}Getting {n} random locations in {str(c).upper()}.{BColors.ENDC}")
    start_time = time.time()

    # Generate random coordinates within the country
    lat_lng_arr = random_points_within_country(c_s, n)
    total_time = time.time() - start_time
    # Print status message with time taken
    print(f"{BColors.OKGREEN}Generated {n} locations in {str(c).upper()} in {BColors.UNDERLINE}{total_time}{BColors.ENDC}{BColors.OKGREEN} seconds. {BColors.ENDC} \n ")
    return lat_lng_arr.tolist()


def save_coordinates_to_json(data, filename="coordinates.json"):
    # Save coordinates to a JSON file
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
    print(f"{BColors.OKGREEN}{BColors.BOLD}Coordinates saved to {filename}{BColors.ENDC}")


def load_countries_shapefiles(countries_list):
    country_shapes_temp = {}
    print(f"{BColors.WARNING}Preparing to load shape files...{BColors.ENDC}")
    for country_name in countries_list:
        # Load shapefile for each country
        print(f"Loading {country_name}.shp...")
        shapefile = f'../../CountryShapes/{country_name}/{country_name}.shp'
        country_gdf = gpd.read_file(shapefile)
        country_shapes_temp[country_name] = country_gdf.unary_union
    print(f"{BColors.OKGREEN}Completed! Starting point generation.{BColors.ENDC} \n")
    return country_shapes_temp


# Load country-radius data from JSON file
with open('./countries_and_search_radius.json', 'r') as f:
    country_search_radius = json.load(f)

countries = [c['name'] for c in country_search_radius]

allocated_images_filename = "./allocated_images_20000.json"
with open(allocated_images_filename, 'r') as infile:
    allocated_images = json.load(infile)

all_coordinates = {}
country_shapes = load_countries_shapefiles(countries)

for targetCountry in countries:
    country_shape = country_shapes[targetCountry]
    num_images = allocated_images.get(targetCountry, 0)
    coordinates = get_coordinate_list(targetCountry, country_shape, num_images)

    # Save coordinates to the dictionary
    all_coordinates[targetCountry] = coordinates

# Save coordinates for all countries to a single JSON file
save_coordinates_to_json(all_coordinates)

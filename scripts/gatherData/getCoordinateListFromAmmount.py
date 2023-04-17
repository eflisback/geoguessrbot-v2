import datetime
from generateRandomLatLng import random_points_within_country
import geopandas as gpd
import json
import time


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_coordinate_list(c, c_s, n):
    print(f"{BColors.OKBLUE}Getting {n} random locations in {str(c).upper()}.{BColors.ENDC}")
    start_time = time.time()

    lat_lng_arr = random_points_within_country(c_s, n)
    total_time = time.time() - start_time
    print(f"{BColors.OKGREEN}"
          f"Generated {n} locations in {str(c).upper()} in {BColors.UNDERLINE}{total_time}"
          f"{BColors.ENDC}{BColors.OKGREEN} seconds. {BColors.ENDC} \n ")
    return lat_lng_arr.tolist()


def save_coordinates_to_json(data, filename="coordinates.json"):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
    print(f"{BColors.OKGREEN}{BColors.BOLD}Coordinates saved to {filename}{BColors.ENDC}")


def load_countries_shapefiles(countries_list):
    country_shapes_temp = {}
    print(f"{BColors.WARNING}Preparing to load shape files...{BColors.ENDC}")
    for country_name in countries_list:
        print(f"Loading {country_name}.shp...")
        shapefile = f'../../CountryShapes/{country_name}/{country_name}.shp'
        country_gdf = gpd.read_file(shapefile)
        country_shapes_temp[country_name] = country_gdf.unary_union
    print(f"{BColors.OKGREEN}Completed! Starting point generation.{BColors.ENDC} \n")
    return country_shapes_temp


# Replace path with country-radius file
with open('./countries_and_search_radius.json', 'r') as f:
    country_search_radius = json.load(f)

countries = [c['name'] for c in country_search_radius]

all_coordinates = {}

runtime_start = time.time()
number_of_locations = 1

country_shapes = load_countries_shapefiles(countries)

for targetCountry in countries:
    country_shape = country_shapes[targetCountry]
    radius = next((c['radius'] for c in country_search_radius if c['name'] == targetCountry), None)
    coordinates = get_coordinate_list(targetCountry, country_shape, number_of_locations)

    # Save coordinates to the dictionary
    all_coordinates[targetCountry] = coordinates

# Save coordinates for all countries to a single JSON file
save_coordinates_to_json(all_coordinates)
runtime_total = time.time() - runtime_start
print(f"Total runtime: {BColors.OKCYAN}{str(datetime.timedelta(seconds=round(runtime_total)))}{BColors.ENDC}. If you were to \
generate {BColors.OKBLUE}{(number_of_locations * 10)}{BColors.ENDC} images per country, it would take approximately \
{BColors.FAIL}{str(datetime.timedelta(seconds=10 * round(runtime_total)))}{BColors.ENDC} instead.")

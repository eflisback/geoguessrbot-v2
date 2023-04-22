from shapely import MultiPoint
import numpy as np

# This script generates random points within a specified country's boundary
# using the Shapely library to handle geometric operations.


# Function to generate random points within the boundary of a given country
# Inputs:
#   country: Shapely geometry object representing the country's boundary
#   n: number of random points to generate
def random_points_within_country(country, n):
    # Get the bounding box of the country
    min_x, min_y, max_x, max_y = country.bounds

    result_points = []
    while len(result_points) < n:
        num_points_to_generate = n - len(result_points)
        print(f"   Generating {num_points_to_generate} random points in rectangle...")

        # Generate random x and y coordinates within the bounding box
        random_x = np.random.uniform(min_x, max_x, num_points_to_generate)
        random_y = np.random.uniform(min_y, max_y, num_points_to_generate)

        # Create MultiPoint geometry from the random x and y coordinates
        random_points = MultiPoint(np.column_stack((random_x, random_y)))

        # Filter points that are contained within the country's boundary
        contained_points = [point for point in random_points.geoms if country.contains(point)]

        # Add contained points to the result_points list
        result_points.extend(contained_points)

    # Convert the result_points list to a numpy array and return it
    return np.array([(point.y, point.x) for point in result_points])

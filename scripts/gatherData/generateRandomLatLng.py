import random
from shapely import MultiPoint
from shapely.geometry import Point
import numpy as np


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


def random_points_within_country(country, n):
    min_x, min_y, max_x, max_y = country.bounds

    result_points = []
    while len(result_points) < n:
        num_points_to_generate = n - len(result_points)
        print(f"   Generating {num_points_to_generate} random points in rectangle...")
        random_x = np.random.uniform(min_x, max_x, num_points_to_generate)
        random_y = np.random.uniform(min_y, max_y, num_points_to_generate)
        random_points = MultiPoint(np.column_stack((random_x, random_y)))

        contained_points = [point for point in random_points.geoms if country.contains(point)]

        result_points.extend(contained_points)

    return np.array([(point.y, point.x) for point in result_points])

import json
import random
import os

# Define the target number of coordinates for each cell
target_coords = 455

# Load the grid data from the JSON file
with open("filtered_grid.json", "r") as f:
    grid = json.load(f)

# Generate random coordinates for each cell
cell_coords = {}
for cell_name, cell_data in grid.items():
    # Get the number of images in the cell subdir
    cell_subdir = os.path.join("../../data/grid/training", cell_name)
    num_images = len([f for f in os.listdir(cell_subdir) if os.path.isfile(os.path.join(cell_subdir, f))])

    # Calculate the number of coordinates to generate for this cell
    num_coords = max(target_coords - num_images, 0)
    print(f"Generating {num_coords} for {cell_name}")

    coords = []
    for i in range(num_coords):
        lat = random.uniform(cell_data["min_lat"], cell_data["max_lat"])
        lon = random.uniform(cell_data["min_lon"], cell_data["max_lon"])
        coords.append([lat, lon])
    cell_coords[cell_name] = coords

# Write the cell coordinates to a new JSON file
with open("cellCoordinates.json", "w") as f:
    json.dump(cell_coords, f)

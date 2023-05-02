import json
import random

# Define the number of coordinates to generate in each cell
num_coords = 200

# Load the grid data from the JSON file
with open("filtered_grid.json", "r") as f:
    grid = json.load(f)

# Generate random coordinates for each cell
cell_coords = {}
for cell_name, cell_data in grid.items():
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

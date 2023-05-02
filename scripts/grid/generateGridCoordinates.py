import json
import math

# Define the bounding box of Europe
europe_bounding_box = {
    "min_lon": -21.0,
    "max_lon": 42.0,
    "min_lat": 35.0,
    "max_lat": 71.0,
}


def create_grid(num_cells_x):
    # Calculate the width of each cell
    cell_width = (europe_bounding_box["max_lon"] - europe_bounding_box["min_lon"]) / num_cells_x

    # Initialize the dictionary of cells
    cells = {}

    # Iterate over the cells
    for i in range(num_cells_x):
        # Calculate the maximum and minimum longitude values for this cell
        max_lon = europe_bounding_box["min_lon"] + (i + 1) * cell_width
        min_lon = europe_bounding_box["min_lon"] + i * cell_width

        # Determine the number of cells on the y-axis
        num_cells_y = math.ceil((europe_bounding_box["max_lat"] - europe_bounding_box["min_lat"]) / cell_width)

        # Iterate over the cells on the y-axis
        for j in range(num_cells_y):
            # Calculate the maximum and minimum latitude values for this cell
            max_lat = europe_bounding_box["min_lat"] + (j + 1) * cell_width
            min_lat = europe_bounding_box["min_lat"] + j * cell_width

            # Create a name for this cell based on its position in the grid
            name = chr(ord('A') + i) + str(j)

            # Add this cell to the dictionary
            cells[name] = {
                "max_lat": max_lat,
                "min_lat": min_lat,
                "max_lon": max_lon,
                "min_lon": min_lon,
            }

    return cells


# Create the grid
grid = create_grid(10)

# Write the grid to a JSON file
with open("grid.json", "w") as f:
    json.dump(grid, f)

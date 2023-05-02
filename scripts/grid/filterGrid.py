import json
import shutil

# Define the list of cells to exclude
exclude_cells = ["A0", "B0-B7", "F2-H4"]

# Load the grid data from the JSON file
with open("grid.json", "r") as f:
    grid = json.load(f)

# Remove the cells specified in the exclude list
for item in exclude_cells:
    if "-" in item:
        # The item is a range of cells
        start, end = item.split("-")
        start_col, start_row = start[0], int(start[1:])
        end_col, end_row = end[0], int(end[1:])
        for col in range(ord(start_col), ord(end_col) + 1):
            for row in range(start_row, end_row + 1):
                cell_name = chr(col) + str(row)
                grid.pop(cell_name, None)
    else:
        # The item is a single cell
        grid.pop(item, None)

# Write the filtered grid to a new JSON file
shutil.copyfile("grid.json", "filtered_grid.json")
with open("filtered_grid.json", "w") as f:
    json.dump(grid, f)

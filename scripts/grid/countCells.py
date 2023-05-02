import json

# Load the JSON data from a file
with open("filtered_grid.json", "r") as f:
    data = json.load(f)

# Count the number of keys in the top-level dictionary
num_cells = len(data.keys())

# Print the result
print(f"The JSON file contains {num_cells} cells.")

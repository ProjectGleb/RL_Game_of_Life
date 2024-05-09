from pathlib import Path
import numpy as np


def load_and_convert_grid():
    grid_list = []  # This will hold all rows of the grid
    with open('/Users/gleb/Desktop/CS/Projects/Game_of_life/text_file.txt', 'r') as file:
        for line in file:
            # Check if the line contains grid characters; adjust condition as needed
            if '•' in line or '*' in line:
                # Create a list representing the row, ignoring spaces
                row = [char for char in line.strip() if char in ('•', '*')]
                grid_list.append(row)
    
    # Before converting to a NumPy array, let's ensure all rows are of the same length
    # This step might not be necessary if your grids are well-formed, but it's a good sanity check
    if not all(len(row) == len(grid_list[0]) for row in grid_list):
        raise ValueError("Not all rows are of the same length.")
    
    # Now, we can safely convert grid_list to a NumPy array
    grid_array = np.array(grid_list)

    return grid_array


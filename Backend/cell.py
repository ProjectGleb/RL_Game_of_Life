from pathlib import Path
import os
import numpy as np
import time
import multiprocessing as mp 


class Cell:
    def __init__(self, numpy_grid):
        self.numpy_grid = numpy_grid

    def select_cells(self):
        while True:
            selection = input("What cell would you like to select [r,c]? Type 'Start' once done.\nInput: ")
            if selection.lower() == "start":
                break  # Exiting the loop
            r, c = map(int, selection.split(','))  # Splitting the input into row and column
            if 0 <= r < len(self.numpy_grid) and 0 <= c < len(self.numpy_grid[0]):
                self.numpy_grid[r][c] = '*'  # Marking the cell as alive
            else:
                print('Invalid selection. Please enter a valid cell within the numpy_grid.')
            os.system('cls' if os.name == 'nt' else 'clear')
            for row in self.numpy_grid:
                print(' '.join(row))
            print()    
        return(self.numpy_grid) 

    #Count the number of surrounding cells for each cell WITHIN THE GRIDS BOUNDARIES (based on the cell) and stores the count.
    def count_surrounding_cells(self, r, c):
        num_rows, num_columns = self.numpy_grid.shape
        alive_count = 0
        for i in range(max(0, r-1), min(r+2, num_rows)):
            for j in range(max(0, c-1), min(c+2, num_columns)):
                if (i, j) != (r, c) and self.numpy_grid[i][j] == '*':
                    alive_count += 1
        return alive_count
    




import numpy as np
import multiprocessing as mp 
from multiprocessing import Pool
from .cell import Cell
import time
import os
from pathlib import Path


class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def create_grid(self):
        numpy_grid = np.empty((self.y, self.x), dtype=object)  # creating an empty array
        for r in range(self.y):  # for every row
            for c in range(self.x):  # for every column
                numpy_grid[r][c] = '•'  # Initializing each cell as not alive

        return numpy_grid
    
    #Specifies how many rows and columns there are in the grid for future use
    def rows_columns (self):
        return self.x, self.y        

    #Splits the grid into 4 quadrants and gives each grid a name (g0,g1, g3, g4)
    def split_grid(self, numpy_grid):

        #Number of collumns in a grid
        rows = numpy_grid.shape[0]
        cols = numpy_grid.shape[1]

        #Finding the grids middle    
        middle_rows = int(rows//2)
        middle_cols = int(cols//2)

        grid1 = numpy_grid[:middle_rows+1,:middle_cols+1]
        grid2 = numpy_grid[middle_rows-1:,:middle_cols+1]
        grid3 = numpy_grid[:middle_rows+1,middle_cols-1:]
        grid4 = numpy_grid[middle_rows-1:,middle_cols-1:]
        return (grid1, grid2, grid3, grid4)
    

    #Assembles the grids 
    def recombine_grids(self, grid1, grid2, grid3, grid4):
        # Combine top-left and bottom-left vertically
        left_side = np.concatenate((grid1, grid2), axis=0)
        # Combine top-right and bottom-right vertically
        right_side = np.concatenate((grid3, grid4), axis=0)
        # Combine the left and right sides horizontally to get the full grid
        combined_grid = np.concatenate((left_side, right_side), axis=1)
        return combined_grid

        
    #Computes number of living neighbours and returns it
    @staticmethod
    def grid_processing(grid):
        num_rows, num_columns = grid.shape
        # Initialize a matrix of zeros with the same shape as numpy_grid to store the counts
        alive_count = np.zeros((num_rows, num_columns), dtype=int)
        
        #Proccessess all cells one by one
        for r in range(num_rows):
            for c in range(num_columns):
                # Check each of the 8 possible neighbors
                for row in range(max(0, r-1), min(r+2, num_rows)):
                    for col in range(max(0, c-1), min(c+2, num_columns)):
                        if (row, col) != (r, c) and grid[row][col] == '*':
                            alive_count[r][c] += 1

        return alive_count
    

    @staticmethod
    def trimming(grid, index_r, index_c):
        # Get the number of rows and columns in the grid
        num_rows, num_cols = grid.shape
        if num_rows > 0:
            grid = np.delete(grid, index_r, axis=0)

        # Remove the last column if it exists
        if num_cols > 0:
            grid = np.delete(grid, index_c, axis=1)
        return grid


    @staticmethod
    def multi_processing(grids):
        start = time.time()
        with Pool(4) as pool:
            result = pool.map(Grid.grid_processing, grids)
        end = time.time()
        print("Processing time:", end - start)
        return result


    #Taking in a number grid and converting it to starts and dots
    def update_grid(self, grid, count_grid):
        num_rows, num_columns = grid.shape
        updated_grid = np.empty((num_rows, num_columns), dtype=object)  # Corrected dtype and used shape directly from grid
        
        #Taking in a number grid and converting it to starts and dots
        for r in range(num_rows):
            for c in range(num_columns):
                alive = count_grid[r][c] == '*'
                neighbors = grid[r][c]
                
                if alive and (neighbors < 2 or neighbors > 3):
                    updated_grid[r][c] = '•'  # Dies
                elif not alive and neighbors == 3:
                    updated_grid[r][c] = '*'  # Becomes alive
                elif alive and (neighbors == 2 or neighbors == 3):
                    updated_grid[r][c] = '*'  # Lives
                else:
                    updated_grid[r][c] = '•'  # Remains dead or dies
        # Joinig elements of each row 
        for row in updated_grid:
            print(' '.join(row))
        print()    
        return(updated_grid) 
    
    
    @staticmethod
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
                        
                    

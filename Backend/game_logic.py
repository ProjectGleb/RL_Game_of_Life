from cell import Cell
from grid import Grid
from pathlib import Path
import time

#Asks if the game should start
def start():
        game_on = input('Would you like to start the game? Y/N: ').lower()
        return game_on == 'y'

#GAME LOGIC
def game_logic(x, y, num_of_generations):
        if __name__ == '__main__':
                if start():  # Check if the game should start
                        count = 0 #Counting generations
                        grid_instance = Grid(x, y)
                        # grid_array = grid_instance.load_and_convert_grid()
                        # new_grid = grid_instance.create_grid() #Create grid
                        r,c = grid_instance.rows_columns()  # Gets number of rows and collumns bassed on the grid_instance
                        cell = Cell(grid_array)
                        # selected_grid = cell.select_cells() #Select cells
                        while count != num_of_generations:


                                segments = grid_instance.split_grid(grid_array) #Creating a tuple of 4 grids (g1,g2,g3,g4)
                                
                                proccessed_grids = grid_instance.multi_processing(segments)  # Processess all 4 segments
                                grid4_processed = grid_instance.trimming(proccessed_grids[3], 0, 0)
                                grid1_processed = grid_instance.trimming(proccessed_grids[0], -1,-1)
                                grid2_processed = grid_instance.trimming(proccessed_grids[1], 0, -1)
                                grid3_processed = grid_instance.trimming(proccessed_grids[2], -1, 0)
                                combined_grid = grid_instance.recombine_grids(grid1_processed, grid2_processed, grid3_processed, grid4_processed)
                                # print(combined_grid)  ###prints the number grid
                                converted_grid = grid_instance.update_grid(combined_grid, grid_array)
                                print(f'Generation {count}')
                                count+=1        
                                grid_array = converted_grid
                                time.sleep(0.2)
                        #Count how many live cels are left on the screen and print the output

        #CALL PROCCESS EXECUTION

game_logic(10, 10, 30)
        


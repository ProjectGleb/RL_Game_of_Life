from pathlib import Path
import time
from logic.API.app import GridDimensions, update_grid_size, process_cells, router
from logic.Backend.cell import Cell
from logic.Backend.grid import Grid
from fastapi.middleware.cors import CORSMiddleware
from logic.Database import database 
from logic.Database.database import Base, get_db, engine, SessionLocal, LiveCells, GridSize
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from logic.Database.database import Base  # Ensure Base is imported from the file where models are defined
from sqlalchemy.orm import Session
#some change

#IMPORTNG ROUTERS
from fastapi import FastAPI,  Response, status, HTTPException, Depends, FastAPI
from logic.API import app

app = FastAPI()

#creeates the db
# Assuming 'database' is the module where your ORM models are defined
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods including OPTIONS
    allow_headers=["*"],  # Allows all headers
)


# CRUD!!!
app.include_router(router)  # Include the router
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#FUNCTION TO QUIRY THE DATABASE FOR LIVE CELLS STORE IT IN VARIABLE 
def getting_db_cells():
    db = SessionLocal()
    try:
        retrieved_live_cells = db.query(LiveCells).all()

        cells_list = []  # Initialize as an empty list
        for cell in retrieved_live_cells:
            cells_list.append([cell.x_position, cell.y_position])
        return cells_list  # It's a good practice to return the data as well.
    finally:
        db.close()

# # Execute the function and print the result
live_cells = getting_db_cells()

# FUNCTION TO QUIRY THE DATABASE FOR LIVE CELLS STORE IT IN VARIABLE 
def getting_db_grid():
    db = SessionLocal()
    try:
        # Query to retrieve all entries of GridSize
        retrieved_gridsize = db.query(GridSize).all()
        grid_size = []
        for gridsize in retrieved_gridsize:
            grid_size.append((gridsize.rows, gridsize.columns))
        grid_size = grid_size[0]
        return grid_size

        print(grid_size)
    finally:
        db.close()

rows, columns = getting_db_grid()
        

def main():
    db = SessionLocal()  # Manually create a session
    try:
        game_logic(x=columns, y=rows, num_of_generations=10, db=db)
    finally:
        db.close()


#Asks if the game should start
# def start():
#         game_on = input('Would you like to start the game? Y/N: ').lower()
#         return game_on == 'y'


############## BEFORRE GETTING THE GRID PROCESSED 1. FEEL CELLS INTO SELECT CELLS FUNCTION
##############


#GAME LOGIC
def game_logic(x, y, num_of_generations,db: Session):
        if __name__ == '__main__':
        # if start():  # Check if the game should start
                count = 0 #Counting generations
                grid_instance = Grid(x, y)
                # grid_array = grid_instance.load_and_convert_grid() ### UPLOADS A GRID #would need to replace new_grid variable with grid_array in the following methods to get it to work
                new_grid = grid_instance.create_grid() #Create grid
                r,c = grid_instance.rows_columns()  # Gets number of rows and collumns bassed on the grid_instance



                cell = Cell(new_grid)
                # selected_grid = cell.select_cells() #Select cells

                #turns grids cell into a selected live cell (if there is one)!!!
                for live_cell in live_cells:
                        x, y = live_cell
                        new_grid[x][y] = '*'

                while count != num_of_generations:
                        segments = grid_instance.split_grid(new_grid) #Creating a tuple of 4 grids (g1,g2,g3,g4)
                        proccessed_grids = grid_instance.multi_processing(segments)  # Processess all 4 segments
                        grid4_processed = grid_instance.trimming(proccessed_grids[3], 0, 0)
                        grid1_processed = grid_instance.trimming(proccessed_grids[0], -1,-1)
                        grid2_processed = grid_instance.trimming(proccessed_grids[1], 0, -1)
                        grid3_processed = grid_instance.trimming(proccessed_grids[2], -1, 0)
                        combined_grid = grid_instance.recombine_grids(grid1_processed, grid2_processed, grid3_processed, grid4_processed)
                        # print(combined_grid)  ###prints the number grid
                        converted_grid = grid_instance.update_grid(combined_grid, new_grid)
                        print(f'Generation {count}')
                        count+=1        
                        new_grid = converted_grid
                        time.sleep(0.1)
                if count == num_of_generations:
                        live_cells_after = []
                        # Count how many cells are alive
                        for row_idx, row in enumerate(new_grid):
                                for col_idx, cell in enumerate(row):
                                        if cell == '*':
                                                live_cells_after.append((row_idx, col_idx))  # Append the x, y coordinates
                ###delete dataset. 
                ### upload new cells 
                # Properly using the 'db' session object now
                db.query(LiveCells).delete()
                db.commit()                 
                              
        
                return(live_cells_after)
                #Count how many live cels are left on the screen and print the output

        #CALL PROCCESS EXECUTION
game_logic(columns, rows, 10, db = db)

####################################### THIS WILL MAKE DELETING THE CELLS FROM DATASET WORK BUT WILL OVERCOMPLICATE IT
# # Main execution
# if __name__ == '__main__':
#     # Create a session for use with the function
#     db = SessionLocal()
#     try:
#         # Call your game logic with the session
#         game_logic(x=columns, y=rows, num_of_generations=10, db=db)
#     finally:
#         # Ensure the session is closed after use
#         db.close()


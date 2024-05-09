from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel
router = APIRouter()
from typing import List
from ..Database.database import get_db, LiveCells, GridSize
from ..Database import database

class GridDimensions(BaseModel):
    rows: int
    columns: int

crud_grid = {"rows": None, "columns": None}
live_cells = []  # Global list to store cell positions


class CellPositions(BaseModel):
    positions: List[List[int]]

###Create a database?
class CellInput(BaseModel):
    totalCells: int
    activeCells: List[List[int]]


@router.post("/process_cells/")
def process_cells(cell_input: CellInput, db: Session = Depends(get_db)): 
    # Properly using the 'db' session object now
    db.query(LiveCells).delete()
    db.commit()

    cells = cell_input.activeCells
    print(cells)
    cell_objects = [LiveCells(x_position=cell[0], y_position=cell[1]) for cell in cells] #Corect database insert!
    for cell_object in cell_objects:
        db.add(cell_object)
    db.commit()
    # Optional: Return the created cell data or some confirmation
    return {"status": "Cells added successfully"}


#rows=10 columns=20
@router.post("/update_grid_size/")
async def update_grid_size(data: GridDimensions, db: Session = Depends(get_db)):
       # Properly using the 'db' session object now
    db.query(GridSize).delete()
    db.commit()

    grid_instance = GridSize(rows = data.rows, columns = data.columns)
    db.add(grid_instance)
    db.commit()
    print(data.rows, data.columns)





#[(3, 4), (4, 2), (4, 4), (5, 3), (5, 4)] #####STORE CELLS IN A UPDATED GRID DATASET, PUSH IT BCK TO FRONTEND THROUGH GET REQUEST
@router.post("/update_grid_size/")
async def update_grid_size(data: GridDimensions, db: Session = Depends(get_db)):
       # Properly using the 'db' session object now
    db.query(GridSize).delete()
    db.commit()

    grid_instance = GridSize(rows = data.rows, columns = data.columns)
    db.add(grid_instance)
    db.commit()
    print(data.rows, data.columns)




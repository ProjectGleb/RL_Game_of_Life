
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1352@localhost/fastapi"

#Establishes the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL) #manages both the connectivity and the overall conversation with the database.

#Creates an insteractive session with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
###Creating the dataset in postgressql 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
#borrow the connection from the main.py
from sqlalchemy.ext.declarative import declarative_base

# factory function that maps any table to a uniform database model (styles classes which represent tables in your database).
Base = declarative_base()

class GridSize(Base):
    __tablename__ = 'grid'
    id = Column(Integer, primary_key=True)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)

    # Additional fields for Grid can be added here, for example:

class LiveCells(Base):
    __tablename__ = 'cells'
    id = Column(Integer, primary_key=True)
    x_position = Column(Integer, nullable=False)
    y_position = Column(Integer, nullable=False)
    grid_id = Column(Integer, ForeignKey('grid.id'))
    grid = relationship("GridSize", back_populates="cells") #setting up the relationship between grid and cells

# Set up back_populates on Grid to reference cells
GridSize.cells = relationship("LiveCells", back_populates="grid") #setting up the relationship between cells and grid


Base.metadata.create_all(engine)


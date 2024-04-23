from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods including OPTIONS
    allow_headers=["*"],  # Allows all headers
)


@app.post("/process_cells/")
async def process_cells(request: Request):
    # Retrieve the body as JSON
    data = await request.json()
    print(data)  # This will print the raw JSON data to the console
    return {"received": True, "data": data}

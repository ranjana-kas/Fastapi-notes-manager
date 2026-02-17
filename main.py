# main.py
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException, Request, Query
from typing import List

# Import our custom modules
from schemas import NoteCreate, NoteUpdate, NoteResponse
import services

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup ThreadPool for background tasks
executor = ThreadPoolExecutor(max_workers=2)

app = FastAPI(title="Notes Manager API (Pro Version)")

# --- 1. MIDDLEWARE (Logging) ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Path: {request.url.path} | Method: {request.method} | Time: {process_time:.4f}s")
    
    return response

# --- 2. BACKGROUND TASK FUNCTION ---
def heavy_background_task(note_title: str):
    """
    Simulates a heavy task, like sending an email or analyzing the note.
    We sleep for 2 seconds to prove it doesn't block the API.
    """
    time.sleep(2) 
    logger.info(f"BACKGROUND TASK COMPLETED: Processed note '{note_title}'")

# --- ROUTES ---

@app.post("/notes/", response_model=NoteResponse, status_code=201)
async def create_new_note(note: NoteCreate):
    created_note = await services.create_note(note)
    
    # Fire and forget: Run heavy task in separate thread
    executor.submit(heavy_background_task, created_note["title"])
    
    return created_note

# UPDATED: Added Pagination Query Parameters
@app.get("/notes/", response_model=List[NoteResponse])
async def read_all_notes(
    skip: int = Query(0, description="Number of items to skip"),
    limit: int = Query(10, description="Max number of items to return")
):
    return await services.get_all_notes(skip=skip, limit=limit)

# NEW: Search Endpoint
# Important: Put this ABOVE /notes/{note_id} so "search" isn't treated as an ID
@app.get("/notes/search", response_model=List[NoteResponse])
async def search_notes(query: str):
    return await services.search_notes(query)

@app.get("/notes/{note_id}", response_model=NoteResponse)
async def read_note(note_id: int):
    note = await services.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=NoteResponse)
async def update_existing_note(note_id: int, note_data: NoteUpdate):
    updated_note = await services.update_note(note_id, note_data)
    print(f"Updated Note: {updated_note}")  # Debugging print statement
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note

@app.delete("/notes/{note_id}")
async def delete_existing_note(note_id: int):
    success = await services.delete_note(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}
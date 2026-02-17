# services.py
from typing import List, Optional
from datetime import datetime
from models import Note
from schemas import NoteCreate, NoteUpdate

notes_db: List[Note] = []

def _get_next_id() -> int:
    if not notes_db:
        return 1
    return notes_db[-1]["id"] + 1

async def create_note(note_data: NoteCreate) -> Note:
    new_id = _get_next_id()
    now = datetime.now()
    
    new_note: Note = {
        "id": new_id,
        "title": note_data.title,
        "content": note_data.content,
        "created_at": now,  # <--- Set timestamp
        "updated_at": now   # <--- Set timestamp
    }
    notes_db.append(new_note)
    return new_note

# UPDATED: Added skip (offset) and limit (page size)
async def get_all_notes(skip: int = 0, limit: int = 10) -> List[Note]:
    # Return a slice of the list
    return notes_db[skip : skip + limit]

# NEW: Search Functionality
async def search_notes(query: str) -> List[Note]:
    results = []
    for note in notes_db:
        # Case-insensitive search in title OR content
        if query.lower() in note["title"].lower() or query.lower() in note["content"].lower():
            results.append(note)
    return results

async def get_note_by_id(note_id: int) -> Optional[Note]:
    for note in notes_db:
        if note["id"] == note_id:
            return note
    return None

async def update_note(note_id: int, note_data: NoteUpdate) -> Optional[Note]:
    for index, note in enumerate(notes_db):
        if note["id"] == note_id:
            # Keep original creation date, update the rest
            original_note = notes_db[index]
            
            updated_note: Note = {
                "id": note_id,
                "title": note_data.title,
                "content": note_data.content,
                "created_at": original_note["created_at"], # Preserve creation time
                "updated_at": datetime.now()               # <--- Update timestamp
            }
            notes_db[index] = updated_note
            return updated_note
    return None

async def delete_note(note_id: int) -> bool:
    for index, note in enumerate(notes_db):
        if note["id"] == note_id:
            notes_db.pop(index)
            return True
    return False
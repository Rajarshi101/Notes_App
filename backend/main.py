from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

class Note(BaseModel):
    id: str
    title: str
    content: str
    public: bool = False

notes_db = {}

@app.get("/notes", response_model=List[Note])
def get_notes():
    return list(notes_db.values())

@app.post("/notes", response_model=Note)
def create_note(note: Note):
    if note.id in notes_db:
        raise HTTPException(status_code=400, detail="Note ID already exists")
    notes_db[note.id] = note
    return note

@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: str):
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: str, updated_note: Note):
    if note_id != updated_note.id:
        raise HTTPException(status_code=400, detail="ID mismatch")
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    notes_db[note_id] = updated_note
    return updated_note

@app.delete("/notes/{note_id}")
def delete_note(note_id: str):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    del notes_db[note_id]
    return {"detail": "Note deleted"}

@app.get("/share/{note_id}", response_model=Note)
def share_note(note_id: str):
    note = notes_db.get(note_id)
    if not note or not note.public:
        raise HTTPException(status_code=404, detail="Note not found or not public")
    return note
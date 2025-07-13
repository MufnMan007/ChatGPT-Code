from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json, os

app = FastAPI()

CHARACTER_FILE = "storage/characters.json"
LORE_FILE = "storage/lore.json"
TIMELINE_FILE = "storage/timeline.json"

def load_data(path):
    if not os.path.exists(path):
        with open(path, 'w') as f: json.dump([], f)
    with open(path, 'r') as f:
        return json.load(f)

def save_data(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

# Models
class Character(BaseModel):
    name: str
    race: str
    class_type: str
    backstory: Optional[str] = None

class Lore(BaseModel):
    topic: str
    description: str

class TimelineEvent(BaseModel):
    date: str
    event: str

# Endpoints
@app.post("/character")
def add_character(char: Character):
    data = load_data(CHARACTER_FILE)
    data = [c for c in data if c["name"].lower() != char.name.lower()]
    data.append(char.dict())
    save_data(CHARACTER_FILE, data)
    return {"message": "Character saved."}

@app.get("/character/{name}")
def get_character(name: str):
    data = load_data(CHARACTER_FILE)
    for char in data:
        if char["name"].lower() == name.lower():
            return char
    raise HTTPException(status_code=404, detail="Character not found")

@app.get("/characters")
def list_characters():
    return load_data(CHARACTER_FILE)

@app.post("/lore")
def add_lore(lore: Lore):
    data = load_data(LORE_FILE)
    data = [l for l in data if l["topic"].lower() != lore.topic.lower()]
    data.append(lore.dict())
    save_data(LORE_FILE, data)
    return {"message": "Lore saved."}

@app.get("/lore/{topic}")
def get_lore(topic: str):
    data = load_data(LORE_FILE)
    for l in data:
        if l["topic"].lower() == topic.lower():
            return l
    raise HTTPException(status_code=404, detail="Lore not found")

@app.get("/lore")
def list_lore():
    return load_data(LORE_FILE)

@app.post("/timeline")
def add_event(event: TimelineEvent):
    data = load_data(TIMELINE_FILE)
    data.append(event.dict())
    save_data(TIMELINE_FILE, data)
    return {"message": "Event saved."}

@app.get("/timeline")
def get_timeline():
    return sorted(load_data(TIMELINE_FILE), key=lambda x: x["date"])
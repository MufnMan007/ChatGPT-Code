from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import json, os

app = FastAPI()

# Ensure storage folder exists
os.makedirs("storage", exist_ok=True)

# Patch OpenAPI with correct server
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Master GPT Archive",
        version="1.0.0",
        description="Store and retrieve characters, lore, and events for D&D.",
        routes=app.routes,
    )
    openapi_schema["servers"] = [{"url": "https://chatgpt-code.onrender.com"}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

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

@app.get("/", include_in_schema=False)
def root():
    return {"status": "Master GPT Archive is alive."}

@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
def plugin_manifest():
    return FileResponse("plugin/ai-plugin.json", media_type="application/json")

# Character routes
@app.post("/save/char")
def save_char(char: Character):
    data = load_data(CHARACTER_FILE)
    data = [c for c in data if c["name"].lower() != char.name.lower()]
    data.append(char.dict())
    save_data(CHARACTER_FILE, data)
    return {"message": "Character saved."}

@app.get("/load/char/{name}")
def load_char(name: str):
    data = load_data(CHARACTER_FILE)
    for char in data:
        if char["name"].lower() == name.lower():
            return char
    raise HTTPException(status_code=404, detail="Character not found")

@app.get("/list/chars")
def list_chars():
    return load_data(CHARACTER_FILE)

# Lore routes
@app.post("/save/lore")
def save_lore(lore: Lore):
    data = load_data(LORE_FILE)
    data = [l for l in data if l["topic"].lower() != lore.topic.lower()]
    data.append(lore.dict())
    save_data(LORE_FILE, data)
    return {"message": "Lore saved."}

@app.get("/load/lore/{topic}")
def load_lore(topic: str):
    data = load_data(LORE_FILE)
    for l in data:
        if l["topic"].lower() == topic.lower():
            return l
    raise HTTPException(status_code=404, detail="Lore not found")

@app.get("/list/lore")
def list_lore():
    return load_data(LORE_FILE)

# Timeline routes
@app.post("/save/event")
def save_event(event: TimelineEvent):
    data = load_data(TIMELINE_FILE)
    data.append(event.dict())
    save_data(TIMELINE_FILE, data)
    return {"message": "Event saved."}

@app.get("/load/events")
def load_events():
    return sorted(load_data(TIMELINE_FILE), key=lambda x: x["date"])
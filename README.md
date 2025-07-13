# Master GPT Archive

An OpenAI-compatible plugin to store and retrieve D&D character data, lore, and timeline events.

## Run locally

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

## Endpoints

- `POST /character` – Add or update a character
- `GET /character/{name}`
- `GET /characters`
- `POST /lore`
- `GET /lore/{topic}`
- `GET /lore`
- `POST /timeline`
- `GET /timeline`
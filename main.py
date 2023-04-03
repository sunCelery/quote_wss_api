import json

from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.websocket('/courses')
async def courses(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        with open('quotes.json', 'r') as f:
            quotes = json.loads(f.read())

        await websocket.send_text(f'{quotes}')

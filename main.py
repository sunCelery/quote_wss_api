import json

from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.websocket('/courses')
async def courses(websocket: WebSocket):
    """
    Endpoint for getting all 3 quotes at once
    """
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        with open('/tmp/quotes.json', 'r') as f:
            quotes = json.loads(f.read())
        await websocket.send_json(quotes)


@app.websocket('/{pair_name:str}')
async def courses(websocket: WebSocket, pair_name: str):
    """
    Defines set of endpoints for getting only one quote
    """
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        with open('/tmp/quotes.json', 'r') as f:
            quotes = json.loads(f.read())
        response = {
                pair_name: f'{quotes[pair_name]}'
            }
        await websocket.send_json(response)

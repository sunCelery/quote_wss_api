import uvicorn
from fastapi import FastAPI, WebSocket
from websocet_cache import CachedResponse


app = FastAPI()


@app.websocket('/courses')
async def courses(websocket: WebSocket):
    """
    Endpoint for getting all 3 quotes at once
    """
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        quotes = cached_response()
        await websocket.send_json(quotes)


@app.websocket('/{pair_name:str}')
async def course(websocket: WebSocket, pair_name: str):
    """
    Defines set of endpoints for getting only one quote
    """
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        quotes = cached_response()
        quote = {pair_name: quotes[pair_name]}
        await websocket.send_json(quote)


if __name__ == '__main__':
    cached_response = CachedResponse()
    uvicorn.run(app, host="0.0.0.0", port=8000)

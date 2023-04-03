import json
import time

import uvicorn
from fastapi import FastAPI, WebSocket, HTTPException

from settings import ACCEPTED_QUOTES

app = FastAPI()


def get_quotes():
    with open('/tmp/quotes.json', 'r') as f:
        quotes = json.loads(f.read())
    return quotes


class CachedResponse:
    __instance = None

    def __call__(self):
        if time.time() - self.cache_timestamp < 10:
            return self.quotes
        else:
            self.__init__()
            return self.quotes

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        CachedResponse.__instance = None

    def __init__(self):
        self.quotes = get_quotes()
        self.cache_timestamp = time.time()


@app.websocket('/courses')
async def courses(websocket: WebSocket):
    """
    Endpoint for getting all 3 quotes at once
    """
    endpoint = websocket.path_params
    # print(f'{dir(websocket)=}')
    # print(f'{endpoint=}')
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        quotes = cached_response()
        await websocket.send_json(quotes)


@app.websocket('/{pair_name:str}')
async def courses(websocket: WebSocket, pair_name: str):
    """
    Defines set of endpoints for getting only one quote
    """
    endpoint = websocket.path_params
    # print(f'{dir(websocket)=}')
    # print(f'{endpoint=}')
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        quotes = cached_response()
        quote = {pair_name: quotes[pair_name]}
        await websocket.send_json(quote)


if __name__ == '__main__':
    cached_response = CachedResponse()
    uvicorn.run(app, host="0.0.0.0", port=8000)

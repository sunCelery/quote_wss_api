import json
import asyncio
from time import sleep
from typing import Callable

import aiohttp
from aiohttp import ClientWebSocketResponse

from settings import (
    URL_OKX, PAYLOADS_OKX, INSTRUMENT_IDS_OKX,
    URL_BINANCE, PAYLOADS_BINANCE, INSTRUMENT_IDS_BINANCE
)


def extract_quote_okx(data: dict) -> dict:
    ticker = data['arg']['instId']
    price = data['data'][0]['last']
    quote = {ticker: price}
    return quote


def extract_quote_binance(data: dict) -> dict:
    ticker = data['s']
    price = data['c']
    quote = {ticker: price}
    return quote


async def wss_connect(url: str,
                      payloads: list,
                      instruments_ids: list) -> None:


    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            while True:
                quotes = instruments_ids.copy()
                for payload in payloads:
                    await ws.send_json(payload)
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)

                            if 'data' in data:
                                ticker = data['arg']['instId']
                                if ticker in quotes:
                                    price = data['data'][0]['last']
                                    quote = {ticker: price}
                                    print(quote)
                                    quotes.remove(ticker)
                                    break

                            elif 's' and 'c' in data:
                                ticker = data['s']
                                if ticker in instruments_ids:
                                    price = data['c']
                                    quote = {ticker: price}
                                    print(quote)
                                    instruments_ids.remove(ticker)
                                    break

                        elif msg.type in (aiohttp.WSMsgType.ERROR,
                                          aiohttp.WSMsgType.CLOSE,
                                          aiohttp.WSMsgType.CLOSED,
                                          aiohttp.WSMsgType.CLOSING):
                            # logging here
                            print(f"WebSocket connection closed "
                                  f"with exception {ws.exception()}")
                            return None
                print()
                sleep(.001)


if __name__ == '__main__':
    while True:
        asyncio.run(wss_connect(URL_OKX, PAYLOADS_OKX, INSTRUMENT_IDS_OKX))
        asyncio.run(wss_connect(URL_BINANCE, PAYLOADS_BINANCE, INSTRUMENT_IDS_BINANCE))


# WSMessage(type=<WSMsgType.TEXT: 1>, data='{"e":"24hrTicker","E":1680476301175,"s":"BTCUSDT","p":"-424.85000000",' \
#                                          '"P":"-1.490","w":"28207.61144018","x":"28515.09000000","c":"28090.09000000",' \
#                                          '"Q":"0.04662000","b":"28090.08000000","B":"3.08774000","a":"28090.09000000",' \
#                                          '"A":"4.26371000","o":"28514.94000000","h":"28555.00000000","l":"27856.43000000",' \
#                                          '"v":"36765.20363000","q":"1037058578.51416150","O":1680389901175,' \
#                                          '"C":1680476301175,"F":3067526919,"L":3068454586,"n":927668}', extra='')
# ticker = data['s']
# price = data['c']


# while True:
#
#     for payload in payloads:
#         await ws.send_json(payload)
#         async for msg in ws:
#             if msg.type == aiohttp.WSMsgType.TEXT:
#                 data = json.loads(msg.data)
#                 print(serializer(data))
#                 break
#             elif msg.type == aiohttp.WSMsgType.ERROR:
#                 print('bad')
#                 print(f"WebSocket connection closed with exception {ws.exception()}")
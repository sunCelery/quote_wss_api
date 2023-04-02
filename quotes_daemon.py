import json
import asyncio
from time import sleep

import aiohttp
from aiohttp import ClientWebSocketResponse


URL_OKX = 'wss://ws.okex.com:8443/ws/v5/public'
INSTRUMENT_IDS_OKX = ['BTC-USDT', 'ETH-USDT', 'XRP-USDT']
PAYLOADS_OKX = [
    {
        "op": "subscribe",
        "args": [
            {
                "channel": "tickers",
                "instId": f"{instrument}",
            }
        ]
    } for instrument in INSTRUMENT_IDS_OKX
]


async def wss_connect(url: str, payloads: list):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            while True:
                for payload in payloads:

                    await ws.send_json(payload)

                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            if 'data' in data:
                                quote_ID = data['arg']['instId']
                                quote = data['data'][0]['last']
                                print({quote_ID: quote})
                                # response = {instrument_ID: f'{quote}'}
                                # return response
                                break
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            print('bad')
                            print(f"WebSocket connection closed with exception {ws.exception()}")
                sleep(5)


if __name__ == '__main__':
    asyncio.run(wss_connect(URL_OKX, PAYLOADS_OKX))
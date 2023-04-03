import asyncio
import json
import sys

import aiohttp

from settings import (
    URL_OKX, PAYLOADS_OKX,
    URL_BINANCE, PAYLOADS_BINANCE,
    QUOTES_CODES
)


async def wss_connect(url: str,
                      payloads: list,
                      quotes_codes: list = QUOTES_CODES,
                      request_frequency: int = 1) -> None:

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            while True:
                quotes = quotes_codes.copy()
                for payload in payloads:
                    await ws.send_json(payload)
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            if 'data' in data:
                                ticker = data['arg']['instId']
                                if ticker in quotes:
                                    price = data['data'][0]['last']
                                    crypto_pairs[ticker] = price
                                    quote = {ticker: price}
                                    quotes.remove(ticker)
                                    break

                            elif 's' in data:
                                ticker = data['s']
                                if ticker in quotes:
                                    price = data['c']
                                    # here need handler to unifi name of quote in JSON
                                    crypto_pairs[ticker] = price
                                    # quote = {ticker: price}
                                    # print(quote)
                                    quotes.remove(ticker)
                                    break

                        elif msg.type in (aiohttp.WSMsgType.ERROR,
                                          aiohttp.WSMsgType.CLOSE,
                                          aiohttp.WSMsgType.CLOSED,
                                          aiohttp.WSMsgType.CLOSING):
                            # logging here
                            print('error')
                            # print(f"WebSocket connection closed "
                            #       f"with exception {ws.exception()}")
                            return None
                with open('quotes.json', 'w') as f:
                    json.dump(crypto_pairs, f)
                print(crypto_pairs)
                await asyncio.sleep(request_frequency)


if __name__ == '__main__':
    try:
        crypto_pairs = {}
        while True:
            asyncio.run(wss_connect(URL_OKX, PAYLOADS_OKX))
            asyncio.run(wss_connect(URL_BINANCE, PAYLOADS_BINANCE))
    except KeyboardInterrupt:
        sys.exit()

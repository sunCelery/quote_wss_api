import asyncio
import json
import sys

import aiohttp

from settings import (
    URL_OKX, PAYLOADS_OKX,
    URL_BINANCE, PAYLOADS_BINANCE,
    QUOTES_CODES
)


def normalize_name(ticker: str) -> str:
    """
    normalize name of ticker on Binance to the same
    as on OKX
    """
    new_ticker_name = ticker[:3] + '-' + ticker[3:]
    return new_ticker_name


async def wss_get_quotes(url: str,
                      payloads: list,
                      quotes_codes: list = QUOTES_CODES,
                      request_frequency: int = 5) -> None:
    """
    Establish main-loop WSS connection with given by url
    exchange server.

    Send requests every request_frequency (default: 5) seconds
    for quotes from quotes_codes list

    Reading WSS response and write it down in temp-scoket like file
    into '/tmp/quotes.json'

    comment:
    This function should be refactored and dived at least for three ones
    """
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
                                    quotes.remove(ticker)
                                    break

                            elif 's' in data:
                                ticker = data['s']
                                if ticker in quotes:
                                    price = data['c']
                                    crypto_pairs[normalize_name(ticker)] = price
                                    quotes.remove(ticker)
                                    break

                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            print('error')
                            # logging here
                            return None

                        elif msg.type in (aiohttp.WSMsgType.CLOSE,
                                          aiohttp.WSMsgType.CLOSED,
                                          aiohttp.WSMsgType.CLOSING):
                            # logging here
                            print('error')
                            # print(f"WebSocket connection closed "
                            #       f"with exception {ws.exception()}")
                            return None
                with open('/tmp/quotes.json', 'w') as f:
                    json.dump(crypto_pairs, f)
                print(crypto_pairs)
                await asyncio.sleep(request_frequency)


def main():
    """
    main-loop that switch WSS connection
    from one exchange to another if connection getting closed
    or have gotten some exchange-server error
    """
    try:
        while True:
            asyncio.run(wss_get_quotes(URL_OKX, PAYLOADS_OKX))
            asyncio.run(wss_get_quotes(URL_BINANCE, PAYLOADS_BINANCE))
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    crypto_pairs = {}
    main()

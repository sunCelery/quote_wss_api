import asyncio
import sys
import datetime
import json
import logging

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

    Reading WSS response and write it down in temp-socket like file
    into '/tmp/quotes.json'

    comment:
    This function should be refactored and dived at least for three ones
    """
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            time_stamp = datetime.datetime.now().strftime('%Y-%M-%d_%X.%f')
            logging.info(f'[ {time_stamp} ] '
                         f'WSS connection to {url} established, '
                         f'collecting quotes every {request_frequency} seconds...')
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
                            time_stamp = datetime.datetime.now().strftime('%Y-%M-%d_%X.%f')
                            logging.error(f'[ {time_stamp} ] '
                                          f'connection to {url} error {ws.exception()}')
                            logging.warning(f'[ {time_stamp} ] '
                                            f'trying to switch connection to another server...')
                            return None

                        elif msg.type in (aiohttp.WSMsgType.CLOSE,
                                          aiohttp.WSMsgType.CLOSED,
                                          aiohttp.WSMsgType.CLOSING):
                            time_stamp = datetime.datetime.now().strftime('%Y-%M-%d_%X.%f')
                            logging.warning(f'[ {time_stamp} ] '
                                            f'WSS connection to {url} closed')
                            logging.warning(f'[ {time_stamp} ] '
                                            f'trying to switch connection to another server...')
                            return None

                with open('/tmp/quotes.json', 'w') as f:
                    json.dump(crypto_pairs, f)
                print(crypto_pairs)
                await asyncio.sleep(request_frequency)


def main() -> None:
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
    logging.basicConfig(level=logging.INFO,
                        filename="log/quotes_daemon.log",
                        filemode="w")
    crypto_pairs = {}
    main()

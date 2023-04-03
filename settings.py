# Both exchanges quote codes
QUOTES_CODES = ['BTC-USDT', 'ETH-USDT', 'XRP-USDT',
                'BTCUSDT', 'ETHUSDT', 'XRPUSDT']

# OKX constants
URL_OKX = 'wss://ws.okex.com:8443/ws/v5/public'
INSTRUMENT_IDS_OKX = ['BTC-USDT', 'ETH-USDT', 'XRP-USDT']
PAYLOADS_OKX = [
    {
        'op': "subscribe",
        'args': [
            {
                'channel': 'tickers',
                'instId': f'{instrument}',
            }
        ]
    } for instrument in INSTRUMENT_IDS_OKX
]

# Binance constants
URL_BINANCE = 'wss://stream.binance.com:9443/ws'
INSTRUMENT_IDS_BINANCE = ['btcusdt@ticker', 'ethusdt@ticker', 'xrpusdt@ticker']
PAYLOADS_BINANCE = [
    {
        'method': "SUBSCRIBE",
        'params': [
            f'{instrument}'
        ],
        'id': 1
    } for instrument in INSTRUMENT_IDS_BINANCE
]

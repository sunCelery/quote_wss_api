import json
import time


def get_quotes():
    """
    Get quotes from file.
    This file is created by quotes_daemon.
    """
    with open('/tmp/quotes.json', 'r') as f:
        quotes = json.loads(f.read())
    return quotes


class CachedResponse:
    """
    Singleton-Functor that cache client's requests
    """
    __instance = None

    def __call__(self, *args, **kwargs):
        if time.time() - self.cache_timestamp < self.lifetime:
            return self.quotes
        else:
            self.__init__(*args, **kwargs)
            return self.quotes

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        CachedResponse.__instance = None

    def __init__(self, lifetime: int = 5):
        """
        :param lifetime: defines time in seconds
        to treat quotes as valid
        """
        self.lifetime = lifetime
        self.quotes = get_quotes()
        self.cache_timestamp = time.time()

    def __init__(self, loop):
        self._loop = loop
        self._exc = None
        self._event = asyncio.Event(loop=loop)
        self._waiters = collections.deque()

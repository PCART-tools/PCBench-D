    def __init__(self, protocol,
                 *, limit=DEFAULT_LIMIT, timer=None, loop=None):
        self._protocol = protocol
        self._low_water = limit
        self._high_water = limit * 2
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._size = 0
        self._cursor = 0
        self._http_chunk_splits = None
        self._buffer = collections.deque()
        self._buffer_offset = 0
        self._eof = False
        self._waiter = None
        self._eof_waiter = None
        self._exception = None
        self._timer = timer
        self._eof_callbacks = []

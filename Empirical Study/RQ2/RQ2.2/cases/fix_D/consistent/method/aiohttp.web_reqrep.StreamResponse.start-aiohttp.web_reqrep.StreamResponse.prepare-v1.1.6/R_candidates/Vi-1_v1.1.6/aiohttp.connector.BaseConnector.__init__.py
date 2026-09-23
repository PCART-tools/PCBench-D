    def __init__(self, *, conn_timeout=None, keepalive_timeout=sentinel,
                 force_close=False, limit=20,
                 loop=None):

        if force_close:
            if keepalive_timeout is not None and \
               keepalive_timeout is not sentinel:
                raise ValueError('keepalive_timeout cannot '
                                 'be set if force_close is True')
        else:
            if keepalive_timeout is sentinel:
                keepalive_timeout = 30

        if loop is None:
            loop = asyncio.get_event_loop()

        self._closed = False
        if loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))

        self._conns = {}
        self._acquired = defaultdict(set)
        self._conn_timeout = conn_timeout
        self._keepalive_timeout = keepalive_timeout
        self._cleanup_handle = None
        self._force_close = force_close
        self._limit = limit
        self._waiters = defaultdict(list)

        self._loop = loop
        self._factory = functools.partial(
            aiohttp.StreamProtocol, loop=loop,
            disconnect_error=ServerDisconnectedError)

        self.cookies = http.cookies.SimpleCookie()

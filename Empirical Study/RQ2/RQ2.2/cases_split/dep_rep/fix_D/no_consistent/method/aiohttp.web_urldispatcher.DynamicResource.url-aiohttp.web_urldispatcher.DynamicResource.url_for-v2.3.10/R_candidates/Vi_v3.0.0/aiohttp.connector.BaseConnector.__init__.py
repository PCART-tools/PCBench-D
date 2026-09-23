    def __init__(self, *, keepalive_timeout=sentinel,
                 force_close=False, limit=100, limit_per_host=0,
                 enable_cleanup_closed=False, loop=None):

        if force_close:
            if keepalive_timeout is not None and \
               keepalive_timeout is not sentinel:
                raise ValueError('keepalive_timeout cannot '
                                 'be set if force_close is True')
        else:
            if keepalive_timeout is sentinel:
                keepalive_timeout = 15.0

        if loop is None:
            loop = asyncio.get_event_loop()

        self._closed = False
        if loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))

        self._conns = {}
        self._limit = limit
        self._limit_per_host = limit_per_host
        self._acquired = set()
        self._acquired_per_host = defaultdict(set)
        self._keepalive_timeout = keepalive_timeout
        self._force_close = force_close
        self._waiters = defaultdict(list)

        self._loop = loop
        self._factory = functools.partial(ResponseHandler, loop=loop)

        self.cookies = SimpleCookie()

        # start keep-alive connection cleanup task
        self._cleanup_handle = None

        # start cleanup closed transports task
        self._cleanup_closed_handle = None
        self._cleanup_closed_disabled = not enable_cleanup_closed
        self._cleanup_closed_transports = []
        self._cleanup_closed()

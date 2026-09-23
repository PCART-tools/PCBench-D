    def __init__(self, *,
                 timeout=10.0, autoclose=True, autoping=True, protocols=()):
        super().__init__(status=101)
        self._protocols = protocols
        self._protocol = None
        self._writer = None
        self._reader = None
        self._closed = False
        self._closing = False
        self._conn_lost = 0
        self._close_code = None
        self._loop = None
        self._waiting = False
        self._exception = None
        self._timeout = timeout
        self._autoclose = autoclose
        self._autoping = autoping

    def __init__(self, *,
                 timeout=10.0, receive_timeout=None,
                 autoclose=True, autoping=True, heartbeat=None,
                 protocols=()):
        super().__init__(status=101)
        self._protocols = protocols
        self._ws_protocol = None
        self._writer = None
        self._reader = None
        self._closed = False
        self._closing = False
        self._conn_lost = 0
        self._close_code = None
        self._loop = None
        self._waiting = None
        self._exception = None
        self._timeout = timeout
        self._receive_timeout = receive_timeout
        self._autoclose = autoclose
        self._autoping = autoping
        self._heartbeat = heartbeat
        self._heartbeat_cb = None
        if heartbeat is not None:
            self._pong_heartbeat = heartbeat/2.0
        self._pong_response_cb = None

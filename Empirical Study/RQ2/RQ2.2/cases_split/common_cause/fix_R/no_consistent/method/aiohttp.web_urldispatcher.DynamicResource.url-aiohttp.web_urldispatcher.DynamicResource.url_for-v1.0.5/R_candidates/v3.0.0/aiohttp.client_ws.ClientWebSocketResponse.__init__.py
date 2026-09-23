    def __init__(self, reader, writer, protocol,
                 response, timeout, autoclose, autoping, loop, *,
                 receive_timeout=None, heartbeat=None,
                 compress=0, client_notakeover=False):
        self._response = response
        self._conn = response.connection

        self._writer = writer
        self._reader = reader
        self._protocol = protocol
        self._closed = False
        self._closing = False
        self._close_code = None
        self._timeout = timeout
        self._receive_timeout = receive_timeout
        self._autoclose = autoclose
        self._autoping = autoping
        self._heartbeat = heartbeat
        self._heartbeat_cb = None
        if heartbeat is not None:
            self._pong_heartbeat = heartbeat/2.0
        self._pong_response_cb = None
        self._loop = loop
        self._waiting = None
        self._exception = None
        self._compress = compress
        self._client_notakeover = client_notakeover

        self._reset_heartbeat()

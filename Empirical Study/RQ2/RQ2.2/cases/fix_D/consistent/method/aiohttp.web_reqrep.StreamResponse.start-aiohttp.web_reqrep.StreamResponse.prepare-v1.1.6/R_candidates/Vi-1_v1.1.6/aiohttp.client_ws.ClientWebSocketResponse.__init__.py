    def __init__(self, reader, writer, protocol,
                 response, timeout, autoclose, autoping, loop):
        self._response = response
        self._conn = response.connection

        self._writer = writer
        self._reader = reader
        self._protocol = protocol
        self._closed = False
        self._closing = False
        self._close_code = None
        self._timeout = timeout
        self._autoclose = autoclose
        self._autoping = autoping
        self._loop = loop
        self._waiting = False
        self._exception = None

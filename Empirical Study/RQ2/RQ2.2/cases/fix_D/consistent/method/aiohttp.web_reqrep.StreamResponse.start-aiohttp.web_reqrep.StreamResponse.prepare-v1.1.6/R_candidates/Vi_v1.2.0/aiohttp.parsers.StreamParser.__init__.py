    def __init__(self, *, loop=None, buf=None,
                 limit=DEFAULT_LIMIT, eof_exc_class=RuntimeError):
        self._loop = loop
        self._eof = False
        self._exception = None
        self._parser = None
        self._output = None
        self._limit = limit
        self._eof_exc_class = eof_exc_class
        self._buffer = buf if buf is not None else ParserBuffer()

        self.paused = False
        self.transport = None

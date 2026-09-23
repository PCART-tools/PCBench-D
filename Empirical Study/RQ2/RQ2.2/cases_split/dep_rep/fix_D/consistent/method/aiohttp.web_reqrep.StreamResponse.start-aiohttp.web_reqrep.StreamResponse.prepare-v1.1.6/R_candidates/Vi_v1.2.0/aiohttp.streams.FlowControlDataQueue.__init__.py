    def __init__(self, stream, *, limit=DEFAULT_LIMIT, loop=None):
        super().__init__(loop=loop)

        self._stream = stream
        self._limit = limit * 2

        # resume transport reading
        if stream.paused:
            try:
                self._stream.transport.resume_reading()
            except (AttributeError, NotImplementedError):
                pass
            else:
                self._stream.paused = False

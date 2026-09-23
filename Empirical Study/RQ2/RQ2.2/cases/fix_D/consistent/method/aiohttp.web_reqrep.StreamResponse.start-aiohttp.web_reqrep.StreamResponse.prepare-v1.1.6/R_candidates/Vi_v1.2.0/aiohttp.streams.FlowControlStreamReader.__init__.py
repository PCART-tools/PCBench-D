    def __init__(self, stream, limit=DEFAULT_LIMIT, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._stream = stream
        self._b_limit = limit * 2

        # resume transport reading
        if stream.paused:
            try:
                self._stream.transport.resume_reading()
            except (AttributeError, NotImplementedError):
                pass
            else:
                self._stream.paused = False

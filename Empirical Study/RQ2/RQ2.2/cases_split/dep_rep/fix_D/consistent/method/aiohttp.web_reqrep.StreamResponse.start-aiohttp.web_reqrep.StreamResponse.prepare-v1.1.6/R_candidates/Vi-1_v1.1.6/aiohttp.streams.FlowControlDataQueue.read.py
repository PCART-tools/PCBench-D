    @asyncio.coroutine
    def read(self):
        result = yield from super().read()

        if self._stream.paused:
            if self._size < self._limit:
                try:
                    self._stream.transport.resume_reading()
                except (AttributeError, NotImplementedError):
                    pass
                else:
                    self._stream.paused = False
        else:
            if self._size > self._limit:
                try:
                    self._stream.transport.pause_reading()
                except (AttributeError, NotImplementedError):
                    pass
                else:
                    self._stream.paused = True

        return result

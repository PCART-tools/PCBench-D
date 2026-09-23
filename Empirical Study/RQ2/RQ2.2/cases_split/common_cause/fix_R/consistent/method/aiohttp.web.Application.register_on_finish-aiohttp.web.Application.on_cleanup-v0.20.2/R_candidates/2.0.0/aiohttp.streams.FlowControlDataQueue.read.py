    @asyncio.coroutine
    def read(self):
        try:
            return (yield from super().read())
        finally:
            if self._size < self._limit and self._protocol._reading_paused:
                self._protocol.resume_reading()

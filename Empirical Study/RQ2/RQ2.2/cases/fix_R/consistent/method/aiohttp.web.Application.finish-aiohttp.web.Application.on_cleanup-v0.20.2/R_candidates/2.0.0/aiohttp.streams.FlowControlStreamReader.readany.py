    @asyncio.coroutine
    def readany(self):
        try:
            return (yield from super().readany())
        finally:
            if self._size < self._b_limit and self._protocol._reading_paused:
                self._protocol.resume_reading()

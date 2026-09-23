    @asyncio.coroutine
    def readexactly(self, n):
        try:
            return (yield from super().readexactly(n))
        finally:
            if self._size < self._b_limit and self._protocol._reading_paused:
                self._protocol.resume_reading()

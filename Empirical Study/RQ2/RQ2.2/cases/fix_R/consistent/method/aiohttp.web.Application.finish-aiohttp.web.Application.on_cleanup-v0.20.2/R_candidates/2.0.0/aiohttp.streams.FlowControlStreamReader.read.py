    @asyncio.coroutine
    def read(self, n=-1):
        try:
            return (yield from super().read(n))
        finally:
            if self._size < self._b_limit and self._protocol._reading_paused:
                self._protocol.resume_reading()

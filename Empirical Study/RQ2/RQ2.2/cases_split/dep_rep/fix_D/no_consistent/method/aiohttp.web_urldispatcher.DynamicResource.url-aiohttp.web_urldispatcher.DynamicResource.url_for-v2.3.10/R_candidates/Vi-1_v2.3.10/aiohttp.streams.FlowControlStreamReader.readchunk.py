    @asyncio.coroutine
    def readchunk(self):
        try:
            return (yield from super().readchunk())
        finally:
            if self._size < self._b_limit and self._protocol._reading_paused:
                self._protocol.resume_reading()

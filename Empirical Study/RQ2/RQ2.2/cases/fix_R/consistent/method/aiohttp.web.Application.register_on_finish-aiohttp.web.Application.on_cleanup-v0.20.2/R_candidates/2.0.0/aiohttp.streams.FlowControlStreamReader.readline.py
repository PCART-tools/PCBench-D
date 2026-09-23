    @asyncio.coroutine
    def readline(self):
        try:
            return (yield from super().readline())
        finally:
            if self._size < self._b_limit and self._protocol._reading_paused:
                self._protocol.resume_reading()

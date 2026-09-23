    def read_nowait(self, n=-1):
        try:
            return super().read_nowait(n)
        finally:
            if self._size < self._b_limit and self._protocol._reading_paused:
                self._protocol.resume_reading()

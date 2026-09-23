    def at_eof(self):
        return self._eof and not self._buffer

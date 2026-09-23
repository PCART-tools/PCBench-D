    @property
    def should_close(self):
        if (self._payload is not None and
                not self._payload.is_eof() or self._upgraded):
            return True

        return (self._should_close or self._upgraded or
                self.exception() is not None or
                self._payload_parser is not None or
                len(self) or self._tail)

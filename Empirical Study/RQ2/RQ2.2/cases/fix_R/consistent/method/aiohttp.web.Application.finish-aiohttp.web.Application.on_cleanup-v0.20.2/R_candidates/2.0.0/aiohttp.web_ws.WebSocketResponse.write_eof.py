    @asyncio.coroutine
    def write_eof(self):
        if self._eof_sent:
            return
        if self._payload_writer is None:
            raise RuntimeError("Response has not been started")

        yield from self.close()
        self._eof_sent = True

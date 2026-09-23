    @asyncio.coroutine
    def drain(self):
        assert not self._eof_sent, "EOF has already been sent"
        assert self._payload_writer is not None, \
            "Response has not been started"
        yield from self._payload_writer.drain()

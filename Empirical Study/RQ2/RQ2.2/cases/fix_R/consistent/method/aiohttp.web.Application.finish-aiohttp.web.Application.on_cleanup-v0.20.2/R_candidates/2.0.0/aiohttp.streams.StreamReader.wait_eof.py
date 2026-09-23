    @asyncio.coroutine
    def wait_eof(self):
        if self._eof:
            return

        assert self._eof_waiter is None
        self._eof_waiter = helpers.create_future(self._loop)
        try:
            yield from self._eof_waiter
        finally:
            self._eof_waiter = None

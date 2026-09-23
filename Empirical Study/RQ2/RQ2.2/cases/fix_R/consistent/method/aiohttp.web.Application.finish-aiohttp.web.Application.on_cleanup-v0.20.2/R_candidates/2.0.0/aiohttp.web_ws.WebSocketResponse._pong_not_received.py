    def _pong_not_received(self):
        self._closed = True
        self._close_code = 1006
        self._exception = asyncio.TimeoutError()

        if self._req is not None:
            self._req.transport.close()

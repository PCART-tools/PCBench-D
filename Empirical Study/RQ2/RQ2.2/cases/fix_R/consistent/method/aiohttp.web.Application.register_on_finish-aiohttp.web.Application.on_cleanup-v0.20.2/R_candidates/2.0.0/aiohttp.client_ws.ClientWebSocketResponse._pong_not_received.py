    def _pong_not_received(self):
        self._closed = True
        self._close_code = 1006
        self._exception = asyncio.TimeoutError()
        self._response.close()

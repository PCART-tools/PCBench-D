    def connection_lost(self, exc):
        super().connection_lost(exc)

        self._closing = True
        if self._request_handler is not None:
            self._request_handler.cancel()

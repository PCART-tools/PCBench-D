    def connection_lost(self, exc):
        self._manager.connection_lost(self, exc)

        super().connection_lost(exc)

        self._manager = None
        self._force_close = True
        self._request_factory = None
        self._request_handler = None
        self._request_parser = None
        self.transport = self.writer = None

        if self._keepalive_handle is not None:
            self._keepalive_handle.cancel()

        for handler in self._request_handlers:
            handler.cancel()

        if self._error_handler is not None:
            self._error_handler.cancel()

        self._request_handlers = ()

        if self._payload_parser is not None:
            self._payload_parser.feed_eof()
            self._payload_parser = None

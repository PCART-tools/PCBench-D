    def connection_lost(self, exc):
        if self._payload_parser is not None:
            try:
                self._payload_parser.feed_eof()
            except Exception:
                pass

        try:
            self._parser.feed_eof()
        except Exception as e:
            if self._payload is not None:
                self._payload.set_exception(
                    ClientPayloadError('Response payload is not completed'))

        if not self.is_eof():
            if isinstance(exc, OSError):
                exc = ClientOSError(*exc.args)
            if exc is None:
                exc = ServerDisconnectedError()
            DataQueue.set_exception(self, exc)

        self.transport = self.writer = None
        self._should_close = True
        self._parser = None
        self._message = None
        self._payload = None
        self._payload_parser = None
        self._reading_paused = False

        super().connection_lost(exc)

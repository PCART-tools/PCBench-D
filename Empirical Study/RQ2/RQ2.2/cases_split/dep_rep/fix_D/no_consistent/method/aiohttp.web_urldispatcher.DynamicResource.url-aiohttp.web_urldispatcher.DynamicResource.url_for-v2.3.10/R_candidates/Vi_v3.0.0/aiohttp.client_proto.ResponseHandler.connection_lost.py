    def connection_lost(self, exc):
        if self._payload_parser is not None:
            with suppress(Exception):
                self._payload_parser.feed_eof()

        try:
            uncompleted = self._parser.feed_eof()
        except Exception:
            uncompleted = None
            if self._payload is not None:
                self._payload.set_exception(
                    ClientPayloadError('Response payload is not completed'))

        if not self.is_eof():
            if isinstance(exc, OSError):
                exc = ClientOSError(*exc.args)
            if exc is None:
                exc = ServerDisconnectedError(uncompleted)
            # assigns self._should_close to True as side effect,
            # we do it anyway below
            self.set_exception(exc)

        self.transport = None
        self._should_close = True
        self._parser = None
        self._message = None
        self._payload = None
        self._payload_parser = None
        self._reading_paused = False

        super().connection_lost(exc)

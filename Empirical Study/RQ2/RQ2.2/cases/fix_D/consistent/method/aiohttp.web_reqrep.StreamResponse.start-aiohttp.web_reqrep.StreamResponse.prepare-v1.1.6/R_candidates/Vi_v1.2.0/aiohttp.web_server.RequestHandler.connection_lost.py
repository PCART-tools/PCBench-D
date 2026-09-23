    def connection_lost(self, exc):
        self._manager.connection_lost(self, exc)

        super().connection_lost(exc)
        self._request_factory = None
        self._manager = None
        self.time_service = None
        self._handler = None

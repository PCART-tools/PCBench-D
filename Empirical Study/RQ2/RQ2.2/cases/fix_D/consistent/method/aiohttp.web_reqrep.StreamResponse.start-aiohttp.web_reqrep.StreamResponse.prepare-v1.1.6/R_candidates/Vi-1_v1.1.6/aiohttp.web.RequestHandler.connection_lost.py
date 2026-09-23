    def connection_lost(self, exc):
        self._manager.connection_lost(self, exc)

        super().connection_lost(exc)

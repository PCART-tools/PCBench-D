    def connection_made(self, transport):
        super().connection_made(transport)

        self._manager.connection_made(self, transport)

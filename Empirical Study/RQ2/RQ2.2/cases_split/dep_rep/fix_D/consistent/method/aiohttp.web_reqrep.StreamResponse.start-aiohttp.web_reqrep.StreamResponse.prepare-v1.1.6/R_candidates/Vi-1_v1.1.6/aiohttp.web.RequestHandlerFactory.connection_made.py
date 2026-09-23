    def connection_made(self, handler, transport):
        self._connections[handler] = transport

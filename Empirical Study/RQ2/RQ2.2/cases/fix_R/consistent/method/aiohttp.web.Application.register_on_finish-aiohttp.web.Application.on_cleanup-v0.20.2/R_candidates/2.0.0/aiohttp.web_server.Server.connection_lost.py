    def connection_lost(self, handler, exc=None):
        if handler in self._connections:
            del self._connections[handler]

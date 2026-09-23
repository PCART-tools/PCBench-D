    def disconnect(self):
        """Disconnect the callbacks."""
        for disconnector in self._disconnectors:
            disconnector()

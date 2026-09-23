    @property
    def closed(self):
        return self._protocol is None or not self._protocol.is_connected()

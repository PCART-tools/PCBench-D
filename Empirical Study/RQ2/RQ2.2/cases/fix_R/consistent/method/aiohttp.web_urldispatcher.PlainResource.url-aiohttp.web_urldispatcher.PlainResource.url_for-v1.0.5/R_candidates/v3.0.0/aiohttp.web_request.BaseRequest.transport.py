    @property
    def transport(self):
        if self._protocol is None:
            return None
        return self._protocol.transport

    def set(self, exc=None):
        self._exc = exc
        self._event.set()

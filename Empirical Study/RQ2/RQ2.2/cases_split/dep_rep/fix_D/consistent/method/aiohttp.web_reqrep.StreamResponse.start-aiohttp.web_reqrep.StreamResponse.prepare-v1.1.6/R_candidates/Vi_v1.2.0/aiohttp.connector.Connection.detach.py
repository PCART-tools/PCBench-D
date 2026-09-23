    def detach(self):
        if self._transport is not None:
            self._connector._release_acquired(self._key, self._transport)
        self._transport = None

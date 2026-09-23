    def release(self):
        if self._transport is not None:
            self._connector._release(
                self._key, self._request, self._transport, self._protocol,
                should_close=False)
            self._transport = None

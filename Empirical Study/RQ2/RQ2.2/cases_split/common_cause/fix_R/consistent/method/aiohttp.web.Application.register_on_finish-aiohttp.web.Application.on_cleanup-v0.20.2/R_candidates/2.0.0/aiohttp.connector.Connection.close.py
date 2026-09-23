    def close(self):
        self._notify_release()

        if self._protocol is not None:
            self._connector._release(
                self._key, self._protocol, should_close=True)
            self._protocol = None

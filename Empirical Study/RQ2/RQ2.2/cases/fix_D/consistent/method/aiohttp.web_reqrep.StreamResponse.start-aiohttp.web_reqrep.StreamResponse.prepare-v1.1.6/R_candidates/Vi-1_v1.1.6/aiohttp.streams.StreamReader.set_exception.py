    def set_exception(self, exc):
        self._exception = exc

        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            if not waiter.cancelled():
                waiter.set_exception(exc)

        canceller = self._canceller
        if canceller is not None:
            self._canceller = None
            canceller.cancel()

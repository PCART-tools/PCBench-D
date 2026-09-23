    def feed_eof(self):
        self._eof = True

        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            if not waiter.cancelled():
                waiter.set_result(True)

        canceller = self._canceller
        if canceller is not None:
            self._canceller = None
            canceller.cancel()

        waiter = self._eof_waiter
        if waiter is not None:
            self._eof_waiter = None
            if not waiter.cancelled():
                waiter.set_result(True)

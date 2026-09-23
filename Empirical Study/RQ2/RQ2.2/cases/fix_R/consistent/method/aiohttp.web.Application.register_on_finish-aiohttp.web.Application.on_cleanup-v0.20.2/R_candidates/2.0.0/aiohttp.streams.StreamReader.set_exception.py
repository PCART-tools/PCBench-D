    def set_exception(self, exc):
        self._exception = exc
        self._eof_callbacks.clear()

        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            if not waiter.done():
                waiter.set_exception(exc)

        waiter = self._eof_waiter
        if waiter is not None:
            self._eof_waiter = None
            if not waiter.done():
                waiter.set_exception(exc)

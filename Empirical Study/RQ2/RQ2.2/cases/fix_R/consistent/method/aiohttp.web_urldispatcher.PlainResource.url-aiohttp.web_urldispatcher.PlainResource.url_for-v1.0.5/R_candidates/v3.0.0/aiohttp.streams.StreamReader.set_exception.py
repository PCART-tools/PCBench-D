    def set_exception(self, exc):
        self._exception = exc
        self._eof_callbacks.clear()

        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            set_exception(waiter, exc)

        waiter = self._eof_waiter
        if waiter is not None:
            set_exception(waiter, exc)
            self._eof_waiter = None

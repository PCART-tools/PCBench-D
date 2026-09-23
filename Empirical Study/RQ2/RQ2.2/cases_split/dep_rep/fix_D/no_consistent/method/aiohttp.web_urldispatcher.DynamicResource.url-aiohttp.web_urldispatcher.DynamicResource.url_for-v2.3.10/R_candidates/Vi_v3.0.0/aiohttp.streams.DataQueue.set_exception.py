    def set_exception(self, exc):
        self._eof = True
        self._exception = exc

        waiter = self._waiter
        if waiter is not None:
            set_exception(waiter, exc)
            self._waiter = None

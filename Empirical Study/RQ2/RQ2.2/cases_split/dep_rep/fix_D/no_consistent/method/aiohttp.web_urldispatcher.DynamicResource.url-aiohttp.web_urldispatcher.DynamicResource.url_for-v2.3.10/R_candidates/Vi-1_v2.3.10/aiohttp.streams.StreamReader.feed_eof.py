    def feed_eof(self):
        self._eof = True

        waiter = self._waiter
        if waiter is not None:
            self._waiter = None
            if not waiter.done():
                waiter.set_result(True)

        waiter = self._eof_waiter
        if waiter is not None:
            self._eof_waiter = None
            if not waiter.done():
                waiter.set_result(True)

        for cb in self._eof_callbacks:
            try:
                cb()
            except Exception:
                internal_logger.exception('Exception in eof callback')

        self._eof_callbacks.clear()

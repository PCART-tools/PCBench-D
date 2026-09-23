    def _notify_waiter_done(self, waiter=None):
        if waiter is None:
            waiter = self._notify_waiter
        if waiter is not None:
            set_result(waiter, True)

        if waiter is self._notify_waiter:
            self._notify_waiter = None

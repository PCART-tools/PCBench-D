    def _notify_waiter_done(self):
        waiter = self._notify_waiter
        if waiter is not None and not waiter.done():
            waiter.set_result(True)

        self._notify_waiter = None

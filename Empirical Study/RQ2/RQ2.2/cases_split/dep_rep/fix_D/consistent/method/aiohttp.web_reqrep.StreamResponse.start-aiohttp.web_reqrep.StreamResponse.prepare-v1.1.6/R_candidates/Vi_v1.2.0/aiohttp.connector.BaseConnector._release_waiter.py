    def _release_waiter(self, key):
        waiters = self._waiters[key]
        while waiters:
            waiter = waiters.pop(0)
            if not waiter.done():
                waiter.set_result(None)
                break

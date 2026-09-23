    def cancel(self):
        """ Cancel all waiters """
        for waiter in self._waiters:
            waiter.cancel()

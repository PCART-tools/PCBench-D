    def force_close(self):
        """Force close connection"""
        self._force_close = True
        for waiter in self._waiters:
            if not waiter.done():
                waiter.cancel()
        if self.transport is not None:
            self.transport.close()
            self.transport = None

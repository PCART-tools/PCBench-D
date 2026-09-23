    def close(self):
        """Stop accepting new pipelinig messages and close
        connection when handlers done processing messages"""
        self._close = True
        for waiter in self._waiters:
            if not waiter.done():
                waiter.cancel()

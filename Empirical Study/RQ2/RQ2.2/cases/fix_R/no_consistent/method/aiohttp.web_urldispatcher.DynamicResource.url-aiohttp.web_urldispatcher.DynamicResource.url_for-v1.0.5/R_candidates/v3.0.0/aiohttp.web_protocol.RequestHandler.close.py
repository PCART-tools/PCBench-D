    def close(self):
        """Stop accepting new pipelinig messages and close
        connection when handlers done processing messages"""
        self._close = True
        if self._waiter:
            self._waiter.cancel()

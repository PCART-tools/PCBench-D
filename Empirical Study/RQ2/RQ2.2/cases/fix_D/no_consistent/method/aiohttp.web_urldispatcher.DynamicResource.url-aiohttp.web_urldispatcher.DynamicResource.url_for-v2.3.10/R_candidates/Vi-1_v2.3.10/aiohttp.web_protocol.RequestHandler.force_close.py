    def force_close(self, send_last_heartbeat=False):
        """Force close connection"""
        self._force_close = True
        for waiter in self._waiters:
            waiter.cancel()
        if self.transport is not None:
            if send_last_heartbeat:
                self.transport.write(b"\r\n")
            self.transport.close()
            self.transport = None

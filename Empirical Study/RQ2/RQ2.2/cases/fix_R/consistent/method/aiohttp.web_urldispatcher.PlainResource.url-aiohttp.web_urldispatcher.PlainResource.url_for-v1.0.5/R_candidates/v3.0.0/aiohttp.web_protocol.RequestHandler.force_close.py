    def force_close(self, send_last_heartbeat=False):
        """Force close connection"""
        self._force_close = True
        if self._waiter:
            self._waiter.cancel()
        if self.transport is not None:
            if send_last_heartbeat:
                self.transport.write(b"\r\n")
            self.transport.close()
            self.transport = None

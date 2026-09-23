    def release(self):
        if self._waiters:
            self.available = False
            writer = self._waiters.pop(0)
            writer.set_transport(self.transport)
        else:
            self.available = True

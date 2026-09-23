    def acquire(self, writer):
        if self.available:
            self.available = False
            writer.set_transport(self.transport)
        else:
            self._waiters.append(writer)

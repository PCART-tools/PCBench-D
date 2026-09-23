    def close(self):
        transport = self.transport
        if transport is not None:
            transport.close()
            self.transport = None
        return transport

    def connection_made(self, transport):
        self.transport = transport
        self.writer = StreamWriter(self, transport, self._loop)

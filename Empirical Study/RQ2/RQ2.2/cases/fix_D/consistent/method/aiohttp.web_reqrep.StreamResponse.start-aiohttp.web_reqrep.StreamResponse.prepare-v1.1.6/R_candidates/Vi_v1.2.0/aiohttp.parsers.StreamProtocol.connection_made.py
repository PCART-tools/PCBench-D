    def connection_made(self, transport):
        self.transport = transport
        self.reader.set_transport(transport)
        self.writer = StreamWriter(transport, self, self.reader, self._loop)

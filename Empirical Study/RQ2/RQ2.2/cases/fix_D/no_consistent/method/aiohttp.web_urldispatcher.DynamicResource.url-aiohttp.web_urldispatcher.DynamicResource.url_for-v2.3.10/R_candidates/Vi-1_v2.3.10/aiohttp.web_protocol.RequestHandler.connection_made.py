    def connection_made(self, transport):
        super().connection_made(transport)

        self.transport = transport
        self.writer = StreamWriter(self, transport, self._loop)

        if self._tcp_keepalive:
            tcp_keepalive(self, transport)

        self.writer.set_tcp_nodelay(True)
        self._manager.connection_made(self, transport)

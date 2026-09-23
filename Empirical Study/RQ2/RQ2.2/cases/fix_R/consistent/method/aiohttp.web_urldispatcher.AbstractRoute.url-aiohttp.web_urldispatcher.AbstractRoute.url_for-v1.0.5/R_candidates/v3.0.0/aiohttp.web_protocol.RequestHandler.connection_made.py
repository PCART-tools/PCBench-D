    def connection_made(self, transport):
        super().connection_made(transport)

        self.transport = transport

        if self._tcp_keepalive:
            tcp_keepalive(transport)

        tcp_cork(transport, False)
        tcp_nodelay(transport, True)
        self._manager.connection_made(self, transport)

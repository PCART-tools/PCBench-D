    def _pre_start(self, request):
        self._loop = request.loop

        headers, protocol, compress, notakeover = self._handshake(
            request)

        self._reset_heartbeat()

        self.set_status(101)
        self.headers.update(headers)
        self.force_close()
        self._compress = compress
        writer = WebSocketWriter(request._protocol,
                                 request._protocol.transport,
                                 compress=compress,
                                 notakeover=notakeover)

        return protocol, writer

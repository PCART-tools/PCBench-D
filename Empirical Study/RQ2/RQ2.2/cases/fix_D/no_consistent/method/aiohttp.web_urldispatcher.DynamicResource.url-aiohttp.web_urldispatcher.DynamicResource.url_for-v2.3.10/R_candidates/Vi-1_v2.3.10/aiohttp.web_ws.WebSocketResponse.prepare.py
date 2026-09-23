    @asyncio.coroutine
    def prepare(self, request):
        # make pre-check to don't hide it by do_handshake() exceptions
        if self._payload_writer is not None:
            return self._payload_writer

        protocol, writer = self._pre_start(request)
        payload_writer = yield from super().prepare(request)
        self._post_start(request, protocol, writer)
        yield from payload_writer.drain()
        return payload_writer

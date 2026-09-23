    @asyncio.coroutine
    def handle_parse_error(self, writer, status, exc=None, message=None):
        request = BaseRequest(
            ERROR, EMPTY_PAYLOAD,
            self, writer, self._time_service, None)

        resp = self.handle_error(request, status, exc, message)
        yield from resp.prepare(request)
        yield from resp.write_eof()

        # Restore default state.
        # Should be no-op if server code didn't touch these attributes.
        self.writer.set_tcp_cork(False)
        self.writer.set_tcp_nodelay(True)

    async def handle_parse_error(self, writer, status, exc=None, message=None):
        request = BaseRequest(
            ERROR, EMPTY_PAYLOAD,
            self, writer, None, self._loop)

        resp = self.handle_error(request, status, exc, message)
        await resp.prepare(request)
        await resp.write_eof()

        if self.transport is not None:
            self.transport.close()

        self._error_handler = None

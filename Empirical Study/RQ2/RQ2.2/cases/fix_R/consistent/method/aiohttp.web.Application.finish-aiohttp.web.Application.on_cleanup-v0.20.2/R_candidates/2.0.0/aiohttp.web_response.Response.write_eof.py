    @asyncio.coroutine
    def write_eof(self):
        body = self._body
        if body is not None:
            if (self._req._method == hdrs.METH_HEAD or
                    self._status in [204, 304]):
                yield from super().write_eof()
            elif self._body_payload:
                yield from body.write(self._payload_writer)
                yield from super().write_eof()
            else:
                yield from super().write_eof(body)
        else:
            yield from super().write_eof()

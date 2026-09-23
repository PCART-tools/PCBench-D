    @asyncio.coroutine
    def write_eof(self):
        if self._eof_sent:
            return
        if self._compressed_body is not None:
            body = self._compressed_body
        else:
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

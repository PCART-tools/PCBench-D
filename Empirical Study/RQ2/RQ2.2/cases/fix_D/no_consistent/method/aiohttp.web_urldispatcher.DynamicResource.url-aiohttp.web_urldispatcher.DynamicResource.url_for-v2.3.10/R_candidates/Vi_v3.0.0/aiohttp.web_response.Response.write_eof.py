    async def write_eof(self):
        if self._eof_sent:
            return
        if self._compressed_body is not None:
            body = self._compressed_body
        else:
            body = self._body
        if body is not None:
            if (self._req._method == hdrs.METH_HEAD or
                    self._status in [204, 304]):
                await super().write_eof()
            elif self._body_payload:
                await body.write(self._payload_writer)
                await super().write_eof()
            else:
                await super().write_eof(body)
        else:
            await super().write_eof()

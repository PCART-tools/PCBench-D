    @asyncio.coroutine
    def write_eof(self):
        body = self._body
        if (body is not None and
                self._req.method != hdrs.METH_HEAD and
                self._status not in [204, 304]):
            self.write(body)
        yield from super().write_eof()

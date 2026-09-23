    async def prepare(self, request):
        if self._eof_sent:
            return
        if self._payload_writer is not None:
            return self._payload_writer

        await request._prepare_hook(self)
        return self._start(request)

    @asyncio.coroutine
    def send(self, ordinal, name, *args, **kwargs):
        yield from self._send(ordinal, name, *args, **kwargs)

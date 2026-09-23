    @asyncio.coroutine
    def write(self, writer):
        yield from self._value(writer)

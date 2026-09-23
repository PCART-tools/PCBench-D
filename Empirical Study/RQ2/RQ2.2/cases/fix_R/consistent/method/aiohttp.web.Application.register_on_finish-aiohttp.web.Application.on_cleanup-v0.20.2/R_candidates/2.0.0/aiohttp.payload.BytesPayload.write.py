    @asyncio.coroutine
    def write(self, writer):
        yield from writer.write(self._value)

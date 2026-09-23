    @asyncio.coroutine
    def write(self, writer):
        chunk = yield from self._value.read(DEFAULT_LIMIT)
        while chunk:
            yield from writer.write(chunk)
            chunk = yield from self._value.read(DEFAULT_LIMIT)

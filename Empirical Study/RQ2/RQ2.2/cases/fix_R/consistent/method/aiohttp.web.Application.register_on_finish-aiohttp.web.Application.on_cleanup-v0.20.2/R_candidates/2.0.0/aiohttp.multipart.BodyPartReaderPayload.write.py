    @asyncio.coroutine
    def write(self, writer):
        field = self._value
        chunk = yield from field.read_chunk(size=2**16)
        while chunk:
            writer.write(field.decode(chunk))
            chunk = yield from field.read_chunk(size=2**16)

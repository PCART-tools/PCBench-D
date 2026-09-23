    @asyncio.coroutine
    def write(self, writer):
        try:
            chunk = self._value.read(DEFAULT_LIMIT)
            while chunk:
                yield from writer.write(chunk.encode(self._encoding))
                chunk = self._value.read(DEFAULT_LIMIT)
        finally:
            self._value.close()

    @asyncio.coroutine
    def write(self, writer):
        while True:
            try:
                chunk = yield from self._value.read()
                if not chunk:
                    break
                yield from writer.write(chunk)
            except EofStream:
                break

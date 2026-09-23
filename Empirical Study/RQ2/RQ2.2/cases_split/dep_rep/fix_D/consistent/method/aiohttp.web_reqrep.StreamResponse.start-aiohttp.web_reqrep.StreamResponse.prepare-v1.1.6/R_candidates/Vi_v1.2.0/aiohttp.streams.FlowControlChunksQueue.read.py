    @asyncio.coroutine
    def read(self):
        try:
            return (yield from super().read())
        except EofStream:
            return b''

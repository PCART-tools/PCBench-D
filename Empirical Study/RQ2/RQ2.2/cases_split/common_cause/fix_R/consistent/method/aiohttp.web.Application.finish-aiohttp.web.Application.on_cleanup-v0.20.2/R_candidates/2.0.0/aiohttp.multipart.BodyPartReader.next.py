    @asyncio.coroutine
    def next(self):
        item = yield from self.read()
        if not item:
            return None
        return item

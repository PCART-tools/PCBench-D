    @asyncio.coroutine
    def next(self):
        """Emits next multipart reader object."""
        item = yield from self.stream.next()
        if self.stream.at_eof():
            yield from self.release()
        return item

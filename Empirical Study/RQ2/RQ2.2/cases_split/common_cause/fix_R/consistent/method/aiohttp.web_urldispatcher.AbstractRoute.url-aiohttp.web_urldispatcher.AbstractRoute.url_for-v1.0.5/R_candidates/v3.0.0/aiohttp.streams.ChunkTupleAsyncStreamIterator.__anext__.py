    async def __anext__(self):
        rv = await self.read_func()
        if rv == (b'', False):
            raise StopAsyncIteration  # NOQA
        return rv

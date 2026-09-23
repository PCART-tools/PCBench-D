    async def __anext__(self):
        part = await self.next()
        if part is None:
            raise StopAsyncIteration  # NOQA
        return part

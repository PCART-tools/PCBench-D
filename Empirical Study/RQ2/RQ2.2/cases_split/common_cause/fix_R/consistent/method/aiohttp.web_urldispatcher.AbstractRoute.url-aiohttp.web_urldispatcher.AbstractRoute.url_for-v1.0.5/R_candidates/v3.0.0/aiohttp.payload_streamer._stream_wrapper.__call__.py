    async def __call__(self, writer):
        await self.coro(writer, *self.args, **self.kwargs)

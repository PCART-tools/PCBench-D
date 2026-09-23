    @asyncio.coroutine
    def __call__(self, writer):
        yield from self.coro(writer, *self.args, **self.kwargs)

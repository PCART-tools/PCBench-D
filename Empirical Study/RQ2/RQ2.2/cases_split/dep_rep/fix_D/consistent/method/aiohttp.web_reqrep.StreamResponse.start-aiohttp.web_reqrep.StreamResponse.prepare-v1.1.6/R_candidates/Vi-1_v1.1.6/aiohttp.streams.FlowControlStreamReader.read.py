    @maybe_resume
    @asyncio.coroutine
    def read(self, n=-1):
        return (yield from super().read(n))

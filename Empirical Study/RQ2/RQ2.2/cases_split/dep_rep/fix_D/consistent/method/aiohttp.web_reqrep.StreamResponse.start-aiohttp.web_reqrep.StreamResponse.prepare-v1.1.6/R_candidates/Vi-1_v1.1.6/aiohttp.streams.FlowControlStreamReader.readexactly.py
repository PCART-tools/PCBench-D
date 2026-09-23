    @maybe_resume
    @asyncio.coroutine
    def readexactly(self, n):
        return (yield from super().readexactly(n))

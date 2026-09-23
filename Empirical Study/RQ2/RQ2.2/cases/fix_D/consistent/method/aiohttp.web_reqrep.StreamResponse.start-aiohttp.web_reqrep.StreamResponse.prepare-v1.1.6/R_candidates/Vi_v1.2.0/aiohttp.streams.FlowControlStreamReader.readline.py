    @maybe_resume
    @asyncio.coroutine
    def readline(self):
        return (yield from super().readline())

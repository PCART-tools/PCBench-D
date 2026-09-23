    @maybe_resume
    @asyncio.coroutine
    def readany(self):
        return (yield from super().readany())

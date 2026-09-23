    @asyncio.coroutine
    def __iter__(self):
        self._awaited = True
        return super().__iter__()

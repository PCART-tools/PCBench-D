    @asyncio.coroutine
    def __iter__(self):
        ret = yield from self._coro
        return ret

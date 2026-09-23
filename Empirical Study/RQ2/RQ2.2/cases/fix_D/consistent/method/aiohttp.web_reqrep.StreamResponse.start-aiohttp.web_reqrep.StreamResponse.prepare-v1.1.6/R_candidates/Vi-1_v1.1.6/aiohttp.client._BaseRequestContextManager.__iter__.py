    @asyncio.coroutine
    def __iter__(self):
        resp = yield from self._coro
        return resp

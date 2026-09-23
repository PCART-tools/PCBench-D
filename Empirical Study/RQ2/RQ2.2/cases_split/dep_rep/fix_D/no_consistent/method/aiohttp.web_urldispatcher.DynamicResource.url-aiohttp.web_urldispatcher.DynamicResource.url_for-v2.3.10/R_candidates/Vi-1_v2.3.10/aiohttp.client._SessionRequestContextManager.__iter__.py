    @asyncio.coroutine
    def __iter__(self):
        try:
            return (yield from self._coro)
        except BaseException:
            yield from self._session.close()
            raise

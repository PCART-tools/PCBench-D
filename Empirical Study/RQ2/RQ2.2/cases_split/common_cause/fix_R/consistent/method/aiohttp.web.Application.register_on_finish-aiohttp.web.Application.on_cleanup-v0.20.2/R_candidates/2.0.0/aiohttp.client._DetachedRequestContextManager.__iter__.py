    @asyncio.coroutine
    def __iter__(self):
        try:
            return (yield from self._coro)
        except:
            self._session.close()
            raise

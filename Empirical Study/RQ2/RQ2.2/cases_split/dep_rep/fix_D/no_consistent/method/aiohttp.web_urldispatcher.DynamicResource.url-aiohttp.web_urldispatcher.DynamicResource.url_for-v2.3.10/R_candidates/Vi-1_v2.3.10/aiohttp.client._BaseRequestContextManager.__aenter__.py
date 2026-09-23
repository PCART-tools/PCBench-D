        @asyncio.coroutine
        def __aenter__(self):
            self._resp = yield from self._coro
            return self._resp

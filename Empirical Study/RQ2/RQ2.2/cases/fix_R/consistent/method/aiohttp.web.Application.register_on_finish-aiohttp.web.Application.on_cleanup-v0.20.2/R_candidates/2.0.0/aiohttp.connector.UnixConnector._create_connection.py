    @asyncio.coroutine
    def _create_connection(self, req):
        _, proto = yield from self._loop.create_unix_connection(
            self._factory, self._path)
        return proto

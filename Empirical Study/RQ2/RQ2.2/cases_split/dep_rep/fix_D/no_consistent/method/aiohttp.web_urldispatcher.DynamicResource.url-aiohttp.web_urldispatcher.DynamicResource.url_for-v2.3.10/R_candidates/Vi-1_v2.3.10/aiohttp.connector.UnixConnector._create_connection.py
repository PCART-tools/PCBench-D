    @asyncio.coroutine
    def _create_connection(self, req):
        try:
            _, proto = yield from self._loop.create_unix_connection(
                self._factory, self._path)
        except OSError as exc:
            raise ClientConnectorError(req.connection_key, exc) from exc

        return proto

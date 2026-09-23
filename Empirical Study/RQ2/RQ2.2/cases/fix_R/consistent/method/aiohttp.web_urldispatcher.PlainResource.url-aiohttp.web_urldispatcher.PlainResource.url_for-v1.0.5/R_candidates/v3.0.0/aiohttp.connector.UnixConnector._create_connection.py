    async def _create_connection(self, req, traces=None):
        try:
            _, proto = await self._loop.create_unix_connection(
                self._factory, self._path)
        except OSError as exc:
            raise ClientConnectorError(req.connection_key, exc) from exc

        return proto

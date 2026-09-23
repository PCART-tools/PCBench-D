    @asyncio.coroutine
    def _create_connection(self, req):
        """Create connection.

        Has same keyword arguments as BaseEventLoop.create_connection.
        """
        if req.proxy:
            _, proto = yield from self._create_proxy_connection(req)
        else:
            _, proto = yield from self._create_direct_connection(req)

        return proto

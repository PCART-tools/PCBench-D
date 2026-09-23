    @asyncio.coroutine
    def _create_connection(self, req):
        """
        Use TCPConnector _create_connection, to emulate old ProxyConnector.
        """
        req.update_proxy(self._proxy, self._proxy_auth)
        transport, proto = yield from super()._create_connection(req)

        return transport, proto

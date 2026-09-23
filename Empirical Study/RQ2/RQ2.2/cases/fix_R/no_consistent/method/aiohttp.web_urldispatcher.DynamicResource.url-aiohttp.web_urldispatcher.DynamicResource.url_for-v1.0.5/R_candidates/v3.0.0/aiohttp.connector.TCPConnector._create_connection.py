    async def _create_connection(self, req, traces=None):
        """Create connection.

        Has same keyword arguments as BaseEventLoop.create_connection.
        """
        if req.proxy:
            _, proto = await self._create_proxy_connection(
                req,
                traces=None
            )
        else:
            _, proto = await self._create_direct_connection(
                req,
                traces=None
            )

        return proto

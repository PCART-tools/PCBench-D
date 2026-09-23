    @asyncio.coroutine
    def ws_connect(self, path, *args, **kwargs):
        """Initiate websocket connection.

        The api corresponds to aiohttp.ClientSession.ws_connect.

        """
        ws = yield from self._session.ws_connect(
            self.make_url(path), *args, **kwargs)
        self._websockets.append(ws)
        return ws

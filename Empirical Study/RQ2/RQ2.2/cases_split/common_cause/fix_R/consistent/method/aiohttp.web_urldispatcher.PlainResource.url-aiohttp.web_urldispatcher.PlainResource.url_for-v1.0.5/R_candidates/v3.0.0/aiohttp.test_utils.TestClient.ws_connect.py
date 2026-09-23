    def ws_connect(self, path, *args, **kwargs):
        """Initiate websocket connection.

        The api corresponds to aiohttp.ClientSession.ws_connect.

        """
        return _WSRequestContextManager(
            self._ws_connect(path, *args, **kwargs)
        )

    async def _ws_connect(self, path, *args, **kwargs):
        ws = await self._session.ws_connect(
            self.make_url(path), *args, **kwargs)
        self._websockets.append(ws)
        return ws

    async def start_server(self):
        await self._server.start_server(loop=self._loop)

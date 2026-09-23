    async def __aenter__(self):
        await self.start_server(loop=self._loop)
        return self

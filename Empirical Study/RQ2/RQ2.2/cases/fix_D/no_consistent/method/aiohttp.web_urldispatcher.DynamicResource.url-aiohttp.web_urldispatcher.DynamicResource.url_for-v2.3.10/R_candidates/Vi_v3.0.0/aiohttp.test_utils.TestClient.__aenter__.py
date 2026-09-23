    async def __aenter__(self):
        await self.start_server()
        return self

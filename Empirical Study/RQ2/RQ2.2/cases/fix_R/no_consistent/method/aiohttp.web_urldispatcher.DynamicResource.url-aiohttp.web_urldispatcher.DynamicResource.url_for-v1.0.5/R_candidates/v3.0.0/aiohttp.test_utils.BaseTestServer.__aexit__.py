    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

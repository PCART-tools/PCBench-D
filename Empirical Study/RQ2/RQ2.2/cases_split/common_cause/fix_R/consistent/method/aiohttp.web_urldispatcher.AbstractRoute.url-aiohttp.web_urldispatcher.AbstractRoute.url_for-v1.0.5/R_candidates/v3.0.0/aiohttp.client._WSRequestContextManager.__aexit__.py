    async def __aexit__(self, exc_type, exc, tb):
        await self._resp.close()

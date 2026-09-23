    async def ping(self, message='b'):
        await self._writer.ping(message)

    async def ping(self, message='b'):
        if self._writer is None:
            raise RuntimeError('Call .prepare() first')
        await self._writer.ping(message)

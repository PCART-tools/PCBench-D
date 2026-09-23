    async def readexactly(self, n):
        raise asyncio.streams.IncompleteReadError(b'', n)

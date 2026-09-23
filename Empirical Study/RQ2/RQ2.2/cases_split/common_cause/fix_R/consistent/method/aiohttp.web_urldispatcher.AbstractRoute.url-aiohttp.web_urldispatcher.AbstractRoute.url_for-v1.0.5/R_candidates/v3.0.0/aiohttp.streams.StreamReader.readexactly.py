    async def readexactly(self, n):
        if self._exception is not None:
            raise self._exception

        blocks = []
        while n > 0:
            block = await self.read(n)
            if not block:
                partial = b''.join(blocks)
                raise asyncio.streams.IncompleteReadError(
                    partial, len(partial) + n)
            blocks.append(block)
            n -= len(block)

        return b''.join(blocks)

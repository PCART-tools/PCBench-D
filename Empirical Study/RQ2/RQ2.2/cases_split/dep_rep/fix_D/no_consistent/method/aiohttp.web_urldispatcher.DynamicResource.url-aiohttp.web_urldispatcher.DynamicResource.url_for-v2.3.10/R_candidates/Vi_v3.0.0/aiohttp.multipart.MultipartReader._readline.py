    async def _readline(self):
        if self._unread:
            return self._unread.pop()
        return await self._content.readline()

    @asyncio.coroutine
    def _readline(self):
        if self._unread:
            return self._unread.pop()
        return (yield from self._content.readline())

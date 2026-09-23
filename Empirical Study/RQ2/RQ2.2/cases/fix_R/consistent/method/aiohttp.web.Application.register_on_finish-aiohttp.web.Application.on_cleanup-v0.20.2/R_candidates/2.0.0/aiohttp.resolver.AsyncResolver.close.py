    @asyncio.coroutine
    def close(self):
        return self._resolver.cancel()

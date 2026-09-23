    async def __aenter__(self):
        self._resp = await self._coro
        return self._resp

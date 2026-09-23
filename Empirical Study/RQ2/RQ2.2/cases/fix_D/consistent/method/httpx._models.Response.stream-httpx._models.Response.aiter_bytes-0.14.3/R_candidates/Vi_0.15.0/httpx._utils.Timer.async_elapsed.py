    async def async_elapsed(self) -> float:
        now = await self._get_time()
        return now - self.started

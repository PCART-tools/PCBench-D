    async def async_start(self) -> None:
        self.started = await self._get_time()

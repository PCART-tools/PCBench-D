    async def aclose(self) -> None:
        if self.close_func is not None:
            await self.close_func()

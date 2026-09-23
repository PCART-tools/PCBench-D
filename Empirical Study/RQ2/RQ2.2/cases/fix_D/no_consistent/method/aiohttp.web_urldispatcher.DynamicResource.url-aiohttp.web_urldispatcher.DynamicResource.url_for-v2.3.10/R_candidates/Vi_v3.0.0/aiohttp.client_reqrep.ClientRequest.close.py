    async def close(self):
        if self._writer is not None:
            try:
                await self._writer
            finally:
                self._writer = None

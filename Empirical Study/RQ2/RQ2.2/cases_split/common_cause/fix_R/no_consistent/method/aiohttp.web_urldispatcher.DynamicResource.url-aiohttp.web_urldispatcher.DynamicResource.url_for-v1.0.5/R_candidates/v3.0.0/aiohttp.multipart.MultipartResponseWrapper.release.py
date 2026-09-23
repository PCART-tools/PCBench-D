    async def release(self):
        """Releases the connection gracefully, reading all the content
        to the void."""
        await self.resp.release()

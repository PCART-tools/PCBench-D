    async def next(self):
        """Emits next multipart reader object."""
        item = await self.stream.next()
        if self.stream.at_eof():
            await self.release()
        return item

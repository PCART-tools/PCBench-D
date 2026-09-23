    async def release(self):
        """Like read(), but reads all the data to the void."""
        if self._at_eof:
            return
        while not self._at_eof:
            await self.read_chunk(self.chunk_size)

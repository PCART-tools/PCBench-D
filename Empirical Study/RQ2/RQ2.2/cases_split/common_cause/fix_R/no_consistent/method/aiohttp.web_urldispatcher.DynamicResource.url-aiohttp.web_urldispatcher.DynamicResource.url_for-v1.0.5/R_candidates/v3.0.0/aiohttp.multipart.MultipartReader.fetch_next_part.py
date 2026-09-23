    async def fetch_next_part(self):
        """Returns the next body part reader."""
        headers = await self._read_headers()
        return self._get_part_reader(headers)

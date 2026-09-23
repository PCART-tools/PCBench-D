    @asyncio.coroutine
    def fetch_next_part(self):
        """Returns the next body part reader."""
        headers = yield from self._read_headers()
        return self._get_part_reader(headers)

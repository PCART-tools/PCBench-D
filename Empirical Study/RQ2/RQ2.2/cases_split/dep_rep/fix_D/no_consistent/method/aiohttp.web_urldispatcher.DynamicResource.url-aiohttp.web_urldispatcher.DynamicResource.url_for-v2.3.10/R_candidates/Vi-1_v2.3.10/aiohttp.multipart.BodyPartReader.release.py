    @asyncio.coroutine
    def release(self):
        """Like :meth:`read`, but reads all the data to the void.

        :rtype: None
        """
        if self._at_eof:
            return
        while not self._at_eof:
            yield from self.read_chunk(self.chunk_size)

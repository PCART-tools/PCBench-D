    @asyncio.coroutine
    def release(self):
        """Like :meth:`read`, but reads all the data to the void.

        :rtype: None
        """
        if self._at_eof:
            return
        if self._length is None:
            while not self._at_eof:
                yield from self.readline()
        else:
            while not self._at_eof:
                yield from self.read_chunk(self.chunk_size)

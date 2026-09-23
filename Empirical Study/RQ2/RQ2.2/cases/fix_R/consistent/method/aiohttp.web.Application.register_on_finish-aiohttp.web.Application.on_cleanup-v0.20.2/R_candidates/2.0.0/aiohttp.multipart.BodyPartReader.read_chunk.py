    @asyncio.coroutine
    def read_chunk(self, size=chunk_size):
        """Reads body part content chunk of the specified size.

        :param int size: chunk size

        :rtype: bytearray
        """
        if self._at_eof:
            return b''
        if self._length:
            chunk = yield from self._read_chunk_from_length(size)
        else:
            chunk = yield from self._read_chunk_from_stream(size)

        self._read_bytes += len(chunk)
        if self._read_bytes == self._length:
            self._at_eof = True
        if self._at_eof:
            assert b'\r\n' == (yield from self._content.readline()), \
                'reader did not read all the data or it is malformed'
        return chunk

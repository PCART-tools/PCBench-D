    @asyncio.coroutine
    def read(self, *, decode=False):
        """Reads body part data.

        :param bool decode: Decodes data following by encoding
                            method from `Content-Encoding` header. If it missed
                            data remains untouched

        :rtype: bytearray
        """
        if self._at_eof:
            return b''
        data = bytearray()
        if self._length is None:
            while not self._at_eof:
                data.extend((yield from self.readline()))
        else:
            while not self._at_eof:
                data.extend((yield from self.read_chunk(self.chunk_size)))
        if decode:
            return self.decode(data)
        return data

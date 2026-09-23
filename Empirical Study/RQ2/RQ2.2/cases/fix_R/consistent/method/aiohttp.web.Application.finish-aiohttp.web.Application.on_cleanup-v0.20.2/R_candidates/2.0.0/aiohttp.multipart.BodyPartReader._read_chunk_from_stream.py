    @asyncio.coroutine
    def _read_chunk_from_stream(self, size):
        """Reads content chunk of body part with unknown length.
        The `Content-Length` header for body part is not necessary.

        :param int size: chunk size

        :rtype: bytearray
        """
        assert size >= len(self._boundary) + 2, \
            'Chunk size must be greater or equal than boundary length + 2'
        first_chunk = self._prev_chunk is None
        if first_chunk:
            self._prev_chunk = yield from self._content.read(size)

        chunk = yield from self._content.read(size)
        self._content_eof += int(self._content.at_eof())
        assert self._content_eof < 3, "Reading after EOF"
        window = self._prev_chunk + chunk
        sub = b'\r\n' + self._boundary
        if first_chunk:
            idx = window.find(sub)
        else:
            idx = window.find(sub, max(0, len(self._prev_chunk) - len(sub)))
        if idx >= 0:
            # pushing boundary back to content
            self._content.unread_data(window[idx:])
            if size > idx:
                self._prev_chunk = self._prev_chunk[:idx]
            chunk = window[len(self._prev_chunk):idx]
            if not chunk:
                self._at_eof = True
        result = self._prev_chunk
        self._prev_chunk = chunk
        return result

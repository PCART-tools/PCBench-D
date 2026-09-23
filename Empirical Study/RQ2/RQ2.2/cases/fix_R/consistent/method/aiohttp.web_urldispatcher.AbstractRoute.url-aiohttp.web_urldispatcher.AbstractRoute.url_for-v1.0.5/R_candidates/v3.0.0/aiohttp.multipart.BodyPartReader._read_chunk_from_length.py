    async def _read_chunk_from_length(self, size):
        # Reads body part content chunk of the specified size.
        # The body part must has Content-Length header with proper value.
        assert self._length is not None, \
            'Content-Length required for chunked read'
        chunk_size = min(size, self._length - self._read_bytes)
        chunk = await self._content.read(chunk_size)
        return chunk

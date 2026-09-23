    async def aread(self) -> bytes:
        """
        Read and return the request content.
        """
        if not hasattr(self, "_content"):
            assert isinstance(self.stream, typing.AsyncIterable)
            self._content = b"".join([part async for part in self.stream])
            # If a streaming request has been read entirely into memory, then
            # we can replace the stream with a raw bytes implementation,
            # to ensure that any non-replayable streams can still be used.
            self.stream = PlainByteStream(self._content)
        return self._content

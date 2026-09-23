    def read(self) -> bytes:
        """
        Read and return the request content.
        """
        if not hasattr(self, "_content"):
            self._content = b"".join(self.stream)
            # If a streaming request has been read entirely into memory, then
            # we can replace the stream with a raw bytes implementation,
            # to ensure that any non-replayable streams can still be used.
            self.stream = ByteStream(self._content)
        return self._content

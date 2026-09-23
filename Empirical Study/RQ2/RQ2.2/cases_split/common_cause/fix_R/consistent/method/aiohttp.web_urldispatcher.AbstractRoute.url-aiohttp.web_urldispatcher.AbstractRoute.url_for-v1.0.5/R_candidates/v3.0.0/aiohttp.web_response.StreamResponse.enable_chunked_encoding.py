    def enable_chunked_encoding(self, chunk_size=None):
        """Enables automatic chunked transfer encoding."""
        self._chunked = True

        if hdrs.CONTENT_LENGTH in self._headers:
            raise RuntimeError("You can't enable chunked encoding when "
                               "a content length is set")
        if chunk_size is not None:
            warnings.warn('Chunk size is deprecated #1615', DeprecationWarning)

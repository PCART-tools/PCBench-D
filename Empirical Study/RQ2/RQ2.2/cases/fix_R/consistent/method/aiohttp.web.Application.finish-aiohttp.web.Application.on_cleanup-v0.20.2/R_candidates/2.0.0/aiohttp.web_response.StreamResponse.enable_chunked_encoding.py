    def enable_chunked_encoding(self, chunk_size=None):
        """Enables automatic chunked transfer encoding."""
        self._chunked = True
        if chunk_size is not None:
            warnings.warn('Chunk size is deprecated #1615', DeprecationWarning)

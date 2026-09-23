    @asyncio.coroutine
    def multipart(self, *, reader=multipart.MultipartReader):
        """Return async iterator to process BODY as multipart."""
        return reader(self._headers, self._payload)

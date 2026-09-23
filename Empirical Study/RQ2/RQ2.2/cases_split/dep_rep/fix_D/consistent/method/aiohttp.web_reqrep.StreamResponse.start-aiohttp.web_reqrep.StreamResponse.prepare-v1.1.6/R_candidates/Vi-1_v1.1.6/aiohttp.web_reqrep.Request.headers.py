    @reify
    def headers(self):
        """A case-insensitive multidict proxy with all headers."""
        return CIMultiDictProxy(self._message.headers)

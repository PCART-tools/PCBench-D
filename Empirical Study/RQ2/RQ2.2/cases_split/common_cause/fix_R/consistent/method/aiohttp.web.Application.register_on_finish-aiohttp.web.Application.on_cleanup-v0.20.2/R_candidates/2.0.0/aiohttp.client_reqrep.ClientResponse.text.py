    @asyncio.coroutine
    def text(self, encoding=None, errors='strict'):
        """Read response payload and decode."""
        if self._content is None:
            yield from self.read()

        if encoding is None:
            encoding = self._get_encoding()

        return self._content.decode(encoding, errors=errors)

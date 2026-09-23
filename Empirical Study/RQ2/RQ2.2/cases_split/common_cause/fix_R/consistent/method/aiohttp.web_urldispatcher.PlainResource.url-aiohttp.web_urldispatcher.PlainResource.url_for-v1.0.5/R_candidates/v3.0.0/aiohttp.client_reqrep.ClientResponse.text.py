    async def text(self, encoding=None, errors='strict'):
        """Read response payload and decode."""
        if self._content is None:
            await self.read()

        if encoding is None:
            encoding = self.get_encoding()

        return self._content.decode(encoding, errors=errors)

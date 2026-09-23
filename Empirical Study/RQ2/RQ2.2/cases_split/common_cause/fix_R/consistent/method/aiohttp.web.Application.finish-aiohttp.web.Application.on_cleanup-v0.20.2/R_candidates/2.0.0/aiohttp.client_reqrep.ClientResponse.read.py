    @asyncio.coroutine
    def read(self):
        """Read response payload."""
        if self._content is None:
            try:
                self._content = yield from self.content.read()
            except:
                self.close()
                raise

        return self._content

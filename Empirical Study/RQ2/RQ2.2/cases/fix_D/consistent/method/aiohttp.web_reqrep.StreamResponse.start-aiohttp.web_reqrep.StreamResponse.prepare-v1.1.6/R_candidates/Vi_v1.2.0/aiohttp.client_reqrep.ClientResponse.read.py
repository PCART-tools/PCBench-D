    @asyncio.coroutine
    def read(self):
        """Read response payload."""
        if self._content is None:
            try:
                self._content = yield from self.content.read()
            except:
                self.close()
                raise
            else:
                yield from self.release()

        return self._content

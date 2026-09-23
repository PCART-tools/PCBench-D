    async def read(self):
        """Read response payload."""
        if self._content is None:
            try:
                self._content = await self.content.read()
            except BaseException:
                self.close()
                raise

        return self._content

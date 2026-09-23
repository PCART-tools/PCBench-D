    @asyncio.coroutine
    def _get_client(self, app):
        """Return a TestClient instance."""
        return TestClient(self.app, loop=self.loop)

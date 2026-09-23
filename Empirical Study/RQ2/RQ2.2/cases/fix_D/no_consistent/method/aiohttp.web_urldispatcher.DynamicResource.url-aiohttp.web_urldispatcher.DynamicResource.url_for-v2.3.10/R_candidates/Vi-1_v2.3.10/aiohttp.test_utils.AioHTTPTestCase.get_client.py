    @asyncio.coroutine
    def get_client(self, server):
        """Return a TestClient instance."""
        return TestClient(server, loop=self.loop)

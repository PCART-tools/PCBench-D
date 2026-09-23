    async def get_server(self, app):
        """Return a TestServer instance."""
        return TestServer(app, loop=self.loop)

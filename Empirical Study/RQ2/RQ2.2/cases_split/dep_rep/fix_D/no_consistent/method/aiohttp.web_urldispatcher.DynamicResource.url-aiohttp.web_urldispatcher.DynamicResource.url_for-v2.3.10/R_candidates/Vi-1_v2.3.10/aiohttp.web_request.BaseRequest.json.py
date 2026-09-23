    @asyncio.coroutine
    def json(self, *, loads=json.loads):
        """Return BODY as JSON."""
        body = yield from self.text()
        return loads(body)

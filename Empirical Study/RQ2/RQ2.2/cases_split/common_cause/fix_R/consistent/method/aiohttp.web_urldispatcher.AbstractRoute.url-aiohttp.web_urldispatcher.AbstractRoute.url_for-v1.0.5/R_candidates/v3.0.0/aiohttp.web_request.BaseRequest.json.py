    async def json(self, *, loads=json.loads):
        """Return BODY as JSON."""
        body = await self.text()
        return loads(body)

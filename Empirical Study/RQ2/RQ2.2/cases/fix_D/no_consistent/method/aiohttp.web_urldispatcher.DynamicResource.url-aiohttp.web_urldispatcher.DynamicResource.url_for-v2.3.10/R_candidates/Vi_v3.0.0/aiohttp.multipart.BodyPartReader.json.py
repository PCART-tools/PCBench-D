    async def json(self, *, encoding=None):
        """Like read(), but assumes that body parts contains JSON data."""
        data = await self.read(decode=True)
        if not data:
            return None
        encoding = encoding or self.get_charset(default='utf-8')
        return json.loads(data.decode(encoding))

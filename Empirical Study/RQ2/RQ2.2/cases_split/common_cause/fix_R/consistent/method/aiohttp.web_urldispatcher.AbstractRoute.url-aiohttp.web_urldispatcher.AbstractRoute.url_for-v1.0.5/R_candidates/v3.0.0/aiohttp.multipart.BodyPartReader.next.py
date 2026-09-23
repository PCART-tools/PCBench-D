    async def next(self):
        item = await self.read()
        if not item:
            return None
        return item

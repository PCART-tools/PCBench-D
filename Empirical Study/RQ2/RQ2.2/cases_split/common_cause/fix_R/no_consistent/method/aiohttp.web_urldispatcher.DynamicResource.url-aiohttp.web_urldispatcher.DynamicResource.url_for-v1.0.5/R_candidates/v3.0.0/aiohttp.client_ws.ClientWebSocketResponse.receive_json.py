    async def receive_json(self, *, loads=json.loads, timeout=None):
        data = await self.receive_str(timeout=timeout)
        return loads(data)

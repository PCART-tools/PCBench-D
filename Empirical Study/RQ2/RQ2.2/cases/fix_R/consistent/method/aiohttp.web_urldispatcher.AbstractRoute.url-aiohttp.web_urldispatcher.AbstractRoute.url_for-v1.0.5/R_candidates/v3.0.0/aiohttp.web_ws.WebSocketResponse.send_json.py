    async def send_json(self, data, compress=None, *, dumps=json.dumps):
        await self.send_str(dumps(data), compress=compress)

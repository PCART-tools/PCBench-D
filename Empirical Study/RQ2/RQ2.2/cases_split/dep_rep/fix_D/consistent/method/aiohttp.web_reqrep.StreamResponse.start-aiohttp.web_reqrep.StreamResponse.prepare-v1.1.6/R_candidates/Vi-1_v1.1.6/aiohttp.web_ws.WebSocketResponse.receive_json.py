    @asyncio.coroutine
    def receive_json(self, *, loads=json.loads):
        data = yield from self.receive_str()
        return loads(data)

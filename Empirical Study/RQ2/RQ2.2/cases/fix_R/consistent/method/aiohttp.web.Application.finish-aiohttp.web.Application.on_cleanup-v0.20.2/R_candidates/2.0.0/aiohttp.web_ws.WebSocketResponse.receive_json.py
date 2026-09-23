    @asyncio.coroutine
    def receive_json(self, *, loads=json.loads, timeout=None):
        data = yield from self.receive_str(timeout=timeout)
        return loads(data)

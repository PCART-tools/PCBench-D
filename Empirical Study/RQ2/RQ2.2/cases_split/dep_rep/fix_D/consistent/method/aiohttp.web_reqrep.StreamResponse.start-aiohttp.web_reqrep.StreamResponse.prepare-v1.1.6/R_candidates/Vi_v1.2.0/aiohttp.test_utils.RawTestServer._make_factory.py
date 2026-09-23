    @asyncio.coroutine
    def _make_factory(self, **kwargs):
        self.handler = Server(self._handler, loop=self._loop, **kwargs)
        return self.handler

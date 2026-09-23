    @asyncio.coroutine
    def _make_factory(self, debug=True, **kwargs):
        self.handler = Server(
            self._handler, loop=self._loop, debug=True, **kwargs)
        return self.handler

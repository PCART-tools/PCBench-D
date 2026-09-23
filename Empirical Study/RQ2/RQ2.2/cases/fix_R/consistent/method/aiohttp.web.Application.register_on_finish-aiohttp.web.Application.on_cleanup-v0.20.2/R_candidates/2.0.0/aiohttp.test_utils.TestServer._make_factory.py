    @asyncio.coroutine
    def _make_factory(self, **kwargs):
        self.handler = self.app.make_handler(loop=self._loop, **kwargs)
        yield from self.app.startup()
        return self.handler

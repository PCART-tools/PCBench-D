    @asyncio.coroutine
    def _make_factory(self, **kwargs):
        self.app._set_loop(self._loop)
        yield from self.app.startup()
        self.handler = self.app.make_handler(loop=self._loop, **kwargs)
        return self.handler

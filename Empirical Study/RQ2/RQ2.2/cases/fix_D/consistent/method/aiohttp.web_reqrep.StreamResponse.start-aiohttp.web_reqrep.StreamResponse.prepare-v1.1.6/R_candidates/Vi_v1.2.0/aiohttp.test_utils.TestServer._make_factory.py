    @asyncio.coroutine
    def _make_factory(self, **kwargs):
        yield from self.app.startup()
        self.handler = self.app.make_handler(**kwargs)
        return self.handler

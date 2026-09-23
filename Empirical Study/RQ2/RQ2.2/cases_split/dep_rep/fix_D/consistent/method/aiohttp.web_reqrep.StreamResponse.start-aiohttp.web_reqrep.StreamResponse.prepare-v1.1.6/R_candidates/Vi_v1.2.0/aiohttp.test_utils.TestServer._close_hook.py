    @asyncio.coroutine
    def _close_hook(self):
        yield from self.app.shutdown()
        yield from self.handler.shutdown()
        yield from self.app.cleanup()

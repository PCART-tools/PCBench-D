    @asyncio.coroutine
    def startup(self):
        """Causes on_startup signal

        Should be called in the event loop along with the request handler.
        """
        yield from self.on_startup.send(self)

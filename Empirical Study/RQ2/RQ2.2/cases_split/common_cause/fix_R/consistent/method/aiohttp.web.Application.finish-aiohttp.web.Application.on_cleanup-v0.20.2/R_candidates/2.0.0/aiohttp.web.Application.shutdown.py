    @asyncio.coroutine
    def shutdown(self):
        """Causes on_shutdown signal

        Should be called before cleanup()
        """
        yield from self.on_shutdown.send(self)

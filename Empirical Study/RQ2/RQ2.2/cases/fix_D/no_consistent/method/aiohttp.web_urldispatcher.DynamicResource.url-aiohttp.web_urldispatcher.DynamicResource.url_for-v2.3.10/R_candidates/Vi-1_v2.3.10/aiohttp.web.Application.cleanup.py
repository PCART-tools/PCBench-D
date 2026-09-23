    @asyncio.coroutine
    def cleanup(self):
        """Causes on_cleanup signal

        Should be called after shutdown()
        """
        yield from self.on_cleanup.send(self)

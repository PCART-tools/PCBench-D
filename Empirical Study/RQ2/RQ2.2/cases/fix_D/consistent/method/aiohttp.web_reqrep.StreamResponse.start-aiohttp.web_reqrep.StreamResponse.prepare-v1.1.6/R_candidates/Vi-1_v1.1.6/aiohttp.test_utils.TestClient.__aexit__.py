        @asyncio.coroutine
        def __aexit__(self, exc_type, exc_value, traceback):
            yield from self.close()

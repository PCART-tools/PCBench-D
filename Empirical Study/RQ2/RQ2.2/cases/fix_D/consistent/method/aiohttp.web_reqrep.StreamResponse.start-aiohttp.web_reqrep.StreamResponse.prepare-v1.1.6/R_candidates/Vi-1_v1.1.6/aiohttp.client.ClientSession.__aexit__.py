        @asyncio.coroutine
        def __aexit__(self, exc_type, exc_val, exc_tb):
            yield from self.close()

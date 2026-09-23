        @asyncio.coroutine
        def __aexit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                yield from self.release()
            else:
                self.close()

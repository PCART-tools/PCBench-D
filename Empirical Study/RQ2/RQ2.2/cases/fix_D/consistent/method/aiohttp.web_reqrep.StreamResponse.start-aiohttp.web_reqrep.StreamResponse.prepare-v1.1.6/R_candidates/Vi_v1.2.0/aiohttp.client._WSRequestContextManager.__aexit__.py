        @asyncio.coroutine
        def __aexit__(self, exc_type, exc, tb):
            yield from self._resp.close()

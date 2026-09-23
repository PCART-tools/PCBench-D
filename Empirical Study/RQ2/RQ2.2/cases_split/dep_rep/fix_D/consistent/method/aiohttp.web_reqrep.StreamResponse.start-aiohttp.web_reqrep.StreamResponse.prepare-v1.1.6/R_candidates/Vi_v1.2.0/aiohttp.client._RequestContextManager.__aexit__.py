        @asyncio.coroutine
        def __aexit__(self, exc_type, exc, tb):
            if exc_type is not None:
                self._resp.close()
            else:
                yield from self._resp.release()

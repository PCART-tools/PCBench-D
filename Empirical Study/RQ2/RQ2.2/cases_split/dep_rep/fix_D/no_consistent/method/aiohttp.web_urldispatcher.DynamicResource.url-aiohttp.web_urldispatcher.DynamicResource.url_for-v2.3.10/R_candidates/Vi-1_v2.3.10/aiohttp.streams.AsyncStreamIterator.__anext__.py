        @asyncio.coroutine
        def __anext__(self):
            try:
                rv = yield from self.read_func()
            except EofStream:
                raise StopAsyncIteration  # NOQA
            if rv == b'':
                raise StopAsyncIteration  # NOQA
            return rv

        @asyncio.coroutine
        def __anext__(self):
            rv = yield from self.read_func()
            if rv == (b'', False):
                raise StopAsyncIteration  # NOQA
            return rv

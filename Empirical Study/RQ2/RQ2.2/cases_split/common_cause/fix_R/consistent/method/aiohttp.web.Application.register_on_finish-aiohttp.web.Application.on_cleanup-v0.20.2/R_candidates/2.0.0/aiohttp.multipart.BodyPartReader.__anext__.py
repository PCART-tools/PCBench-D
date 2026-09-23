        @asyncio.coroutine
        def __anext__(self):
            part = yield from self.next()
            if part is None:
                raise StopAsyncIteration  # NOQA
            return part

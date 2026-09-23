        @asyncio.coroutine
        def __aenter__(self):
            yield from self.start_server(loop=self._loop)
            return self

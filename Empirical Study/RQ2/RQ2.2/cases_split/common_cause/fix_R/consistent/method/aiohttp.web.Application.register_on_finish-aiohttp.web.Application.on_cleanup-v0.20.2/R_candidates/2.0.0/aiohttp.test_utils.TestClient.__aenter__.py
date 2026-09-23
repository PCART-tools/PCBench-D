        @asyncio.coroutine
        def __aenter__(self):
            yield from self.start_server()
            return self

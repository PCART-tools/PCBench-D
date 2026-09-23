    @asyncio.coroutine
    def drain(self):
        if self._resp_impl is None:
            raise RuntimeError("Response has not been started")
        yield from self._resp_impl.transport.drain()

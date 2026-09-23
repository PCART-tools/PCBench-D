    @asyncio.coroutine
    def release(self):
        """Releases the connection gracefully, reading all the content
        to the void."""
        yield from self.resp.release()

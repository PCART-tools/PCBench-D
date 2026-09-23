    @asyncio.coroutine
    def close(self):
        """Close all fixtures created by the test client.

        After that point, the TestClient is no longer usable.

        This is an idempotent function: running close multiple times
        will not have any additional effects.

        close is also run when the object is garbage collected, and on
        exit when used as a context manager.

        """
        if self.started and not self.closed:
            self.server.close()
            yield from self.server.wait_closed()
            self._root = None
            self.port = None
            yield from self._close_hook()
            self._closed = True

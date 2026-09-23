    @asyncio.coroutine
    def close(self):
        """Close all fixtures created by the test client.

        After that point, the TestClient is no longer usable.

        This is an idempotent function: running close multiple times
        will not have any additional effects.

        close is also run when the object is garbage collected, and on
        exit when used as a context manager.

        """
        if self.server is not None and not self._closed:
            self.server.close()
            yield from self.server.wait_closed()
            yield from self.app.shutdown()
            yield from self.handler.finish_connections()
            yield from self.app.cleanup()
            self._root = None
            self.port = None
            self._closed = True

    @asyncio.coroutine
    def shutdown(self, timeout=15.0):
        """Worker process is about to exit, we need cleanup everything and
        stop accepting requests. It is especially important for keep-alive
        connections."""
        if self._request_handler is None:
            return
        self._closing = True

        if self._request_count > 1 and not self._reading_request:
            # force-close idle keep-alive connections
            self._request_handler.cancel()
        elif timeout:
            canceller = self._loop.call_later(timeout,
                                              self._request_handler.cancel)
            with suppress(asyncio.CancelledError):
                yield from self._request_handler
            canceller.cancel()
        else:
            self._request_handler.cancel()

    @asyncio.coroutine
    def shutdown(self, timeout=15.0):
        """Worker process is about to exit, we need cleanup everything and
        stop accepting requests. It is especially important for keep-alive
        connections."""
        self._force_close = True

        if self._keepalive_handle is not None:
            self._keepalive_handle.cancel()

        # cancel waiters
        for waiter in self._waiters:
            waiter.cancel()

        # wait for handlers
        with suppress(asyncio.CancelledError, asyncio.TimeoutError):
            with CeilTimeout(timeout, loop=self._loop):
                if self._error_handler and not self._error_handler.done():
                    yield from self._error_handler

                while True:
                    h = None
                    for handler in self._request_handlers:
                        if not handler.done():
                            h = handler
                            break
                    if h:
                        yield from h
                    else:
                        break

        # force-close non-idle handlers
        for handler in self._request_handlers:
            handler.cancel()

        if self.transport is not None:
            self.transport.close()
            self.transport = None

        if self._request_handlers:
            self._request_handlers.clear()

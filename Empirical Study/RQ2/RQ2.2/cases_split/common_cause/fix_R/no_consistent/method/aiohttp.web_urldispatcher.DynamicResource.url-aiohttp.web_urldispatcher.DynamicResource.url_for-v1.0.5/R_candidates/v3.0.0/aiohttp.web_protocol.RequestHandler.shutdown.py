    async def shutdown(self, timeout=15.0):
        """Worker process is about to exit, we need cleanup everything and
        stop accepting requests. It is especially important for keep-alive
        connections."""
        self._force_close = True

        if self._keepalive_handle is not None:
            self._keepalive_handle.cancel()

        if self._waiter:
            self._waiter.cancel()

        # wait for handlers
        with suppress(asyncio.CancelledError, asyncio.TimeoutError):
            with CeilTimeout(timeout, loop=self._loop):
                if self._error_handler and not self._error_handler.done():
                    await self._error_handler

                if self._task_handler and not self._task_handler.done():
                    await self._task_handler

        # force-close non-idle handler
        if self._task_handler:
            self._task_handler.cancel()

        if self.transport is not None:
            self.transport.close()
            self.transport = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._tasks:
            self._tasks.pop()

        if exc_type is asyncio.CancelledError and self._cancelled:
            raise asyncio.TimeoutError from None

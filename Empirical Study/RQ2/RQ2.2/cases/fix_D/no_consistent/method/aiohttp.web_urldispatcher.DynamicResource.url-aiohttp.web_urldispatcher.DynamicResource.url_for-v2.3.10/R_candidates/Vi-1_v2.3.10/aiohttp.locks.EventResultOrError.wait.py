    @asyncio.coroutine
    def wait(self):
        fut = ensure_future(self._event.wait(), loop=self._loop)
        self._waiters.append(fut)
        try:
            val = yield from fut
        finally:
            self._waiters.remove(fut)

        if self._exc is not None:
            raise self._exc

        return val

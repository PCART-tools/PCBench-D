    async def wait(self):
        waiter = self._loop.create_task(self._event.wait())
        self._waiters.append(waiter)
        try:
            val = await waiter
        finally:
            self._waiters.remove(waiter)

        if self._exc is not None:
            raise self._exc

        return val

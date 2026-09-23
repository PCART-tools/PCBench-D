    def _wait_next_notify(self):
        self._notify_waiter_done()

        self._notify_waiter = waiter = asyncio.Future(loop=self.loop)
        self.loop.call_later(1.0, self._notify_waiter_done)

        return waiter

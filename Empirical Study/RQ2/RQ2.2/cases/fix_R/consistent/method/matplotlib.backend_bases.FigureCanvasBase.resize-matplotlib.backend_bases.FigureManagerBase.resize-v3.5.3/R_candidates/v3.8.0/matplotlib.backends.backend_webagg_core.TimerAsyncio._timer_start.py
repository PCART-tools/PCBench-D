    def _timer_start(self):
        self._timer_stop()

        self._task = asyncio.ensure_future(
            self._timer_task(max(self.interval / 1_000., 1e-6))
        )

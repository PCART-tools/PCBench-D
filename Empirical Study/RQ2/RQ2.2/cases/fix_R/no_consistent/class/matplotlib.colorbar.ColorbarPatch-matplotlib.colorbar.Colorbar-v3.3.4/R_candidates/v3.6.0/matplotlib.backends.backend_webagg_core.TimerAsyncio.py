class TimerAsyncio(backend_bases.TimerBase):
    def __init__(self, *args, **kwargs):
        self._task = None
        super().__init__(*args, **kwargs)

    async def _timer_task(self, interval):
        while True:
            try:
                await asyncio.sleep(interval)
                self._on_timer()

                if self._single:
                    break
            except asyncio.CancelledError:
                break

    def _timer_start(self):
        self._timer_stop()

        self._task = asyncio.ensure_future(
            self._timer_task(max(self.interval / 1_000., 1e-6))
        )

    def _timer_stop(self):
        if self._task is not None:
            self._task.cancel()
        self._task = None

    def _timer_set_interval(self):
        # Only stop and restart it if the timer has already been started
        if self._task is not None:
            self._timer_stop()
            self._timer_start()

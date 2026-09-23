    async def _timer_task(self, interval):
        while True:
            try:
                await asyncio.sleep(interval)
                self._on_timer()

                if self._single:
                    break
            except asyncio.CancelledError:
                break

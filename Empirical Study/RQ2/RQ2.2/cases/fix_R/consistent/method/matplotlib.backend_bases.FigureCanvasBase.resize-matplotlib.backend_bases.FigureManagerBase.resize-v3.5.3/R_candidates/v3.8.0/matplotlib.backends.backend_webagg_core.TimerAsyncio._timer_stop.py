    def _timer_stop(self):
        if self._task is not None:
            self._task.cancel()
        self._task = None

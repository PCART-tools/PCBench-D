    def _timer_set_interval(self):
        if self._timer.IsRunning():
            self._timer_start()  # Restart with new interval.

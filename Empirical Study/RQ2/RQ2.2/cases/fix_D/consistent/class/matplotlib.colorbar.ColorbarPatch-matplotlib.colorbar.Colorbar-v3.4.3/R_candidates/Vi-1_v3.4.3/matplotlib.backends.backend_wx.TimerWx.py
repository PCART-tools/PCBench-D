class TimerWx(TimerBase):
    """Subclass of `.TimerBase` using wx.Timer events."""

    def __init__(self, *args, **kwargs):
        self._timer = wx.Timer()
        self._timer.Notify = self._on_timer
        super().__init__(*args, **kwargs)

    def _timer_start(self):
        self._timer.Start(self._interval, self._single)

    def _timer_stop(self):
        self._timer.Stop()

    def _timer_set_interval(self):
        if self._timer.IsRunning():
            self._timer_start()  # Restart with new interval.

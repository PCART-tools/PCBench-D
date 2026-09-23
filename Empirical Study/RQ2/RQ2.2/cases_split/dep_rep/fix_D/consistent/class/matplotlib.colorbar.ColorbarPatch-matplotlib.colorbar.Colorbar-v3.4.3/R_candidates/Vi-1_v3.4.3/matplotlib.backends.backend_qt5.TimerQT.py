class TimerQT(TimerBase):
    """Subclass of `.TimerBase` using QTimer events."""

    def __init__(self, *args, **kwargs):
        # Create a new timer and connect the timeout() signal to the
        # _on_timer method.
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._on_timer)
        super().__init__(*args, **kwargs)

    def __del__(self):
        # The check for deletedness is needed to avoid an error at animation
        # shutdown with PySide2.
        if not _isdeleted(self._timer):
            self._timer_stop()

    def _timer_set_single_shot(self):
        self._timer.setSingleShot(self._single)

    def _timer_set_interval(self):
        self._timer.setInterval(self._interval)

    def _timer_start(self):
        self._timer.start()

    def _timer_stop(self):
        self._timer.stop()

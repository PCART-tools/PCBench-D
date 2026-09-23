class TimerTk(TimerBase):
    """Subclass of `backend_bases.TimerBase` using Tk timer events."""

    def __init__(self, parent, *args, **kwargs):
        self._timer = None
        super().__init__(*args, **kwargs)
        self.parent = parent

    def _timer_start(self):
        self._timer_stop()
        self._timer = self.parent.after(self._interval, self._on_timer)

    def _timer_stop(self):
        if self._timer is not None:
            self.parent.after_cancel(self._timer)
        self._timer = None

    def _on_timer(self):
        super()._on_timer()
        # Tk after() is only a single shot, so we need to add code here to
        # reset the timer if we're not operating in single shot mode.  However,
        # if _timer is None, this means that _timer_stop has been called; so
        # don't recreate the timer in that case.
        if not self._single and self._timer:
            if self._interval > 0:
                self._timer = self.parent.after(self._interval, self._on_timer)
            else:
                # Edge case: Tcl after 0 *prepends* events to the queue
                # so a 0 interval does not allow any other events to run.
                # This incantation is cancellable and runs as fast as possible
                # while also allowing events and drawing every frame. GH#18236
                self._timer = self.parent.after_idle(
                    lambda: self.parent.after(self._interval, self._on_timer)
                )
        else:
            self._timer = None

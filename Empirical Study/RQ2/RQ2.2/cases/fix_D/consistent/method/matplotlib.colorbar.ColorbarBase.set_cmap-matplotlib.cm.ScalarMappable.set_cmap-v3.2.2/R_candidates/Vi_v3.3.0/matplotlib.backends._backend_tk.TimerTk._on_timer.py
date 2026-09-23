    def _on_timer(self):
        TimerBase._on_timer(self)
        # Tk after() is only a single shot, so we need to add code here to
        # reset the timer if we're not operating in single shot mode.  However,
        # if _timer is None, this means that _timer_stop has been called; so
        # don't recreate the timer in that case.
        if not self._single and self._timer:
            self._timer = self.parent.after(self._interval, self._on_timer)
        else:
            self._timer = None

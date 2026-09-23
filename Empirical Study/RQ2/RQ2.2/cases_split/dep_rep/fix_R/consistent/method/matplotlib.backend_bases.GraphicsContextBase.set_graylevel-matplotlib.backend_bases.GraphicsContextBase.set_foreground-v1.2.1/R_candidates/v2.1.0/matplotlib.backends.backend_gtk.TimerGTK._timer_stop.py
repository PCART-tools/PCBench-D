    def _timer_stop(self):
        if self._timer is not None:
            gobject.source_remove(self._timer)
            self._timer = None

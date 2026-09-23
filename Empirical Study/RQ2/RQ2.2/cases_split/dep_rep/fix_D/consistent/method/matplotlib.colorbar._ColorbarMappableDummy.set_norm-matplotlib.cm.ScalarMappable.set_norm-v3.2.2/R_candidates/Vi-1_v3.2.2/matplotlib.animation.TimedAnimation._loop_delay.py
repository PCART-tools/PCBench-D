    def _loop_delay(self, *args):
        # Reset the interval and change callbacks after the delay.
        self.event_source.remove_callback(self._loop_delay)
        self.event_source.interval = self._interval
        self.event_source.add_callback(self._step)
        Animation._step(self)

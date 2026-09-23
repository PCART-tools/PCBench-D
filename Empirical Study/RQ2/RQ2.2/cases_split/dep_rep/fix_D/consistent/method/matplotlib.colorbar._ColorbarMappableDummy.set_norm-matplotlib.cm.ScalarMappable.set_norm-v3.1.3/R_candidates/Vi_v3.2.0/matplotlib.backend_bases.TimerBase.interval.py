    @interval.setter
    def interval(self, interval):
        # Force to int since none of the backends actually support fractional
        # milliseconds, and some error or give warnings.
        interval = int(interval)
        self._interval = interval
        self._timer_set_interval()

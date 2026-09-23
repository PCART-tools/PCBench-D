    @interval.setter
    def interval(self, interval):
        # Force to int since none of the backends actually support fractional
        # milliseconds, and some error or give warnings.
        # Some backends also fail when interval == 0, so ensure >= 1 msec
        interval = max(int(interval), 1)
        self._interval = interval
        self._timer_set_interval()

    def __init__(self, interval=1, tz=None):
        """
        *interval* is the interval between each iteration.  For
        example, if ``interval=2``, mark every second microsecond.

        """
        self._interval = interval
        self._wrapped_locator = ticker.MultipleLocator(interval)
        self.tz = tz

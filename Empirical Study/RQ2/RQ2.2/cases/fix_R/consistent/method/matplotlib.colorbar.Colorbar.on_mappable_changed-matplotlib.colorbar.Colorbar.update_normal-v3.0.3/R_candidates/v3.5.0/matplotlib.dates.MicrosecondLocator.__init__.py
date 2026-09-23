    def __init__(self, interval=1, tz=None):
        """
        *interval* is the interval between each iteration.  For
        example, if ``interval=2``, mark every second microsecond.

        """
        super().__init__(tz=tz)
        self._interval = interval
        self._wrapped_locator = ticker.MultipleLocator(interval)

    def __init__(self, tz=None, minticks=5, maxticks=None,
                 interval_multiples=True):
        """
        *minticks* is the minimum number of ticks desired, which is used to
        select the type of ticking (yearly, monthly, etc.).

        *maxticks* is the maximum number of ticks desired, which controls
        any interval between ticks (ticking every other, every 3, etc.).
        For really fine-grained control, this can be a dictionary mapping
        individual rrule frequency constants (YEARLY, MONTHLY, etc.)
        to their own maximum number of ticks.  This can be used to keep
        the number of ticks appropriate to the format chosen in
        :class:`AutoDateFormatter`. Any frequency not specified in this
        dictionary is given a default value.

        *tz* is a :class:`tzinfo` instance.

        *interval_multiples* is a boolean that indicates whether ticks
        should be chosen to be multiple of the interval. This will lock
        ticks to 'nicer' locations. For example, this will force the
        ticks to be at hours 0,6,12,18 when hourly ticking is done at
        6 hour intervals.

        The AutoDateLocator has an interval dictionary that maps the
        frequency of the tick (a constant from dateutil.rrule) and a
        multiple allowed for that ticking.  The default looks like this::

          self.intervald = {
            YEARLY  : [1, 2, 4, 5, 10, 20, 40, 50, 100, 200, 400, 500,
                      1000, 2000, 4000, 5000, 10000],
            MONTHLY : [1, 2, 3, 4, 6],
            DAILY   : [1, 2, 3, 7, 14],
            HOURLY  : [1, 2, 3, 4, 6, 12],
            MINUTELY: [1, 5, 10, 15, 30],
            SECONDLY: [1, 5, 10, 15, 30],
            MICROSECONDLY: [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000,
                           5000, 10000, 20000, 50000, 100000, 200000, 500000,
                           1000000],
            }

        The interval is used to specify multiples that are appropriate for
        the frequency of ticking. For instance, every 7 days is sensible
        for daily ticks, but for minutes/seconds, 15 or 30 make sense.
        You can customize this dictionary by doing::

          locator = AutoDateLocator()
          locator.intervald[HOURLY] = [3] # only show every 3 hours
        """
        DateLocator.__init__(self, tz)
        self._locator = YearLocator()
        self._freq = YEARLY
        self._freqs = [YEARLY, MONTHLY, DAILY, HOURLY, MINUTELY,
                       SECONDLY, MICROSECONDLY]
        self.minticks = minticks

        self.maxticks = {YEARLY: 11, MONTHLY: 12, DAILY: 11, HOURLY: 12,
                         MINUTELY: 11, SECONDLY: 11, MICROSECONDLY: 8}
        if maxticks is not None:
            try:
                self.maxticks.update(maxticks)
            except TypeError:
                # Assume we were given an integer. Use this as the maximum
                # number of ticks for every frequency and create a
                # dictionary for this
                self.maxticks = dict.fromkeys(self._freqs, maxticks)
        self.interval_multiples = interval_multiples
        self.intervald = {
            YEARLY:   [1, 2, 4, 5, 10, 20, 40, 50, 100, 200, 400, 500,
                       1000, 2000, 4000, 5000, 10000],
            MONTHLY:  [1, 2, 3, 4, 6],
            DAILY:    [1, 2, 3, 7, 14, 21],
            HOURLY:   [1, 2, 3, 4, 6, 12],
            MINUTELY: [1, 5, 10, 15, 30],
            SECONDLY: [1, 5, 10, 15, 30],
            MICROSECONDLY: [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000,
                            5000, 10000, 20000, 50000, 100000, 200000, 500000,
                            1000000]}
        if interval_multiples:
            # Swap "3" for "4" in the DAILY list; If we use 3 we get bad
            # tick loc for months w/ 31 days: 1, 4,..., 28, 31, 1
            # If we use 4 then we get: 1, 5, ... 25, 29, 1
            self.intervald[DAILY] = [1, 2, 4, 7, 14, 21]

        self._byranges = [None, range(1, 13), range(1, 32),
                          range(0, 24), range(0, 60), range(0, 60), None]

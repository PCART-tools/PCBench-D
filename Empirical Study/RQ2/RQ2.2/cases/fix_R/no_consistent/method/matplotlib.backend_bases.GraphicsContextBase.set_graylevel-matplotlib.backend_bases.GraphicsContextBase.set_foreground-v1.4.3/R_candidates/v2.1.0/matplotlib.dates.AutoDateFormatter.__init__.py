    def __init__(self, locator, tz=None, defaultfmt='%Y-%m-%d'):
        """
        Autoformat the date labels.  The default format is the one to use
        if none of the values in ``self.scaled`` are greater than the unit
        returned by ``locator._get_unit()``.
        """
        self._locator = locator
        self._tz = tz
        self.defaultfmt = defaultfmt
        self._formatter = DateFormatter(self.defaultfmt, tz)
        self.scaled = {DAYS_PER_YEAR: rcParams['date.autoformatter.year'],
                       DAYS_PER_MONTH: rcParams['date.autoformatter.month'],
                       1.0: rcParams['date.autoformatter.day'],
                       1. / HOURS_PER_DAY: rcParams['date.autoformatter.hour'],
                       1. / (MINUTES_PER_DAY):
                           rcParams['date.autoformatter.minute'],
                       1. / (SEC_PER_DAY):
                           rcParams['date.autoformatter.second'],
                       1. / (MUSECONDS_PER_DAY):
                           rcParams['date.autoformatter.microsecond']}

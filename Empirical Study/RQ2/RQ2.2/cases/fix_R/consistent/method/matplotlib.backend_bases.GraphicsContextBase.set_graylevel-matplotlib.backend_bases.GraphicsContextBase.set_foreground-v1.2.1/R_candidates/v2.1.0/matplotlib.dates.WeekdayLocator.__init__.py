    def __init__(self, byweekday=1, interval=1, tz=None):
        """
        Mark every weekday in *byweekday*; *byweekday* can be a number or
        sequence.

        Elements of *byweekday* must be one of MO, TU, WE, TH, FR, SA,
        SU, the constants from :mod:`dateutil.rrule`, which have been
        imported into the :mod:`matplotlib.dates` namespace.

        *interval* specifies the number of weeks to skip.  For example,
        ``interval=2`` plots every second week.
        """
        if isinstance(byweekday, np.ndarray):
            # This fixes a bug in dateutil <= 2.3 which prevents the use of
            # numpy arrays in (among other things) the bymonthday, byweekday
            # and bymonth parameters.
            [x.item() for x in byweekday.astype(int)]

        rule = rrulewrapper(DAILY, byweekday=byweekday,
                            interval=interval, **self.hms0d)
        RRuleLocator.__init__(self, rule, tz)

    def __init__(self, bymonth=None, bymonthday=1, interval=1, tz=None):
        """
        Mark every month in *bymonth*; *bymonth* can be an int or
        sequence.  Default is ``range(1, 13)``, i.e. every month.

        *interval* is the interval between each iteration.  For
        example, if ``interval=2``, mark every second occurrence.
        """
        if bymonth is None:
            bymonth = range(1, 13)
        elif isinstance(bymonth, np.ndarray):
            # This fixes a bug in dateutil <= 2.3 which prevents the use of
            # numpy arrays in (among other things) the bymonthday, byweekday
            # and bymonth parameters.
            bymonth = [x.item() for x in bymonth.astype(int)]

        rule = rrulewrapper(MONTHLY, bymonth=bymonth, bymonthday=bymonthday,
                            interval=interval, **self.hms0d)
        super().__init__(rule, tz)

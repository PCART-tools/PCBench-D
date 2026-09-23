    def __init__(self, base=1, month=1, day=1, tz=None):
        """
        Mark years that are multiple of base on a given month and day
        (default jan 1).
        """
        rule = rrulewrapper(YEARLY, interval=base, bymonth=month,
                            bymonthday=day, **self.hms0d)
        super().__init__(rule, tz)
        self.base = ticker._Edge_integer(base, 0)

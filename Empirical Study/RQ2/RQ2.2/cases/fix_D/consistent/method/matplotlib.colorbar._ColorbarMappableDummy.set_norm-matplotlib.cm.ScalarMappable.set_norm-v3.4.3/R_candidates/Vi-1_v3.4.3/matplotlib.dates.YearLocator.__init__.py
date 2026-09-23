    def __init__(self, base=1, month=1, day=1, tz=None):
        """
        Mark years that are multiple of base on a given month and day
        (default jan 1).
        """
        super().__init__(tz)
        self.base = ticker._Edge_integer(base, 0)
        self.replaced = {'month':  month,
                         'day':    day,
                         'hour':   0,
                         'minute': 0,
                         'second': 0,
                         }
        if not hasattr(tz, 'localize'):
            # if tz is pytz, we need to do this w/ the localize fcn,
            # otherwise datetime.replace works fine...
            self.replaced['tzinfo'] = tz

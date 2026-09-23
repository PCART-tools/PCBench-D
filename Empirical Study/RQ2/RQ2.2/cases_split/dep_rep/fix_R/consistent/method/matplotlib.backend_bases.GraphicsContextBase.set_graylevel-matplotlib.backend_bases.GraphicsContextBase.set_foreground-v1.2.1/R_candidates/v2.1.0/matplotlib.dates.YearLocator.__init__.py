    def __init__(self, base=1, month=1, day=1, tz=None):
        """
        Mark years that are multiple of base on a given month and day
        (default jan 1).
        """
        DateLocator.__init__(self, tz)
        self.base = ticker.Base(base)
        self.replaced = {'month':  month,
                         'day':    day,
                         'hour':   0,
                         'minute': 0,
                         'second': 0,
                         'tzinfo': tz
                         }
